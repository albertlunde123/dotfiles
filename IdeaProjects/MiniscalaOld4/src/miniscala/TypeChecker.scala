package miniscala

import miniscala.Ast.*
import miniscala.Unparser.unparse

/**
  * Type checker for MiniScala.
  */
object TypeChecker {

  type VarTypeEnv = Map[Var, Type]

  type FunTypeEnv = Map[Fun, (List[Type], Type)]

  def typeCheck(e: Exp, vtenv: VarTypeEnv, ftenv: FunTypeEnv): Type = e match {
    case IntLit(_) => IntType()
    case BoolLit(_) => BoolType()
    case FloatLit(_) => FloatType()
    case StringLit(_) => StringType()
    case VarExp(x) =>
      vtenv.get(x) match {
        case Some(t) => t
        case None => throw TypeError("Undefined variable", VarExp(x))
      }
    case BinOpExp(leftexp, op, rightexp) =>
      val lefttype = typeCheck(leftexp, vtenv, ftenv)
      val righttype = typeCheck(rightexp, vtenv, ftenv)
      op match {
        case PlusBinOp() =>
          (lefttype, righttype) match {
            case (IntType(), IntType()) => IntType()
            case (FloatType(), FloatType()) => FloatType()
            case (IntType(), FloatType()) => FloatType()
            case (FloatType(), IntType()) => FloatType()
            case (StringType(), StringType()) => StringType()
            case (StringType(), IntType()) => StringType()
            case (StringType(), FloatType()) => StringType()
            case (IntType(), StringType()) => StringType()
            case (FloatType(), StringType()) => StringType()
            case _ => throw TypeError(s"Type mismatch at '+', unexpected types ${lefttype} and ${righttype}", op)
          }
        case MinusBinOp() | MultBinOp() | DivBinOp() | ModuloBinOp() | MaxBinOp() =>
          (lefttype, righttype) match {
            case (IntType(), IntType()) => IntType()
            case (FloatType(), FloatType()) => FloatType()
            case (IntType(), FloatType()) => FloatType()
            case (FloatType(), IntType()) => FloatType()
            case _ => throw TypeError(s"Type mismatch at ${op} unexpected types ${lefttype} and ${righttype}", op)
          }
        case EqualBinOp() => BoolType()
        case LessThanBinOp() | LessThanOrEqualBinOp() =>
          (lefttype, righttype) match {
            case (IntType(), IntType()) => BoolType()
            case (FloatType(), FloatType()) => BoolType()
            case (IntType(), FloatType()) => BoolType()
            case (FloatType(), IntType()) => BoolType()
            case _ => throw TypeError(s"Type mismatch at ${op} unexpected types ${lefttype} and ${righttype}", op)
          }
        case AndBinOp() | OrBinOp() =>
          (lefttype, righttype) match {
            case (BoolType(), BoolType()) => BoolType()
            case _ => throw TypeError(s"Type mismatch at ${op} unexpected types ${lefttype} and ${righttype}", op)
          }
      }
    case UnOpExp(op, exp) => 
      val exptype = typeCheck(exp, vtenv, ftenv)
      op match {
        case NegUnOp() =>
          exptype match {
            case IntType() => IntType()
            case FloatType() => FloatType()
            case _ => throw TypeError(s"Type mismatch at ${op} unexpected types ${exptype}", op)
          }
        case NotUnOp() =>
          exptype match {
            case BoolType() => BoolType()
            case _ => throw TypeError(s"Type mismatch at ${op} unexpected types ${exptype}", op)
          }
      }
    case IfThenElseExp(condexp, thenexp, elseexp) =>
      val condtype = typeCheck(condexp, vtenv, ftenv)
      if (condtype != BoolType()) {
        throw TypeError("condition should be boolean", condexp)
      }
      val thentype = typeCheck(thenexp, vtenv, ftenv)
      val elsetype = typeCheck(elseexp, vtenv, ftenv)
      if (thentype == elsetype) {
        thentype
      }
      else throw TypeError("then and else statement should be of the same type", e)
    case BlockExp(vals, defs, exp) =>
      var vtenv1 = vtenv
      var ftenv1 = ftenv
      for (d <- vals) {
        val t = typeCheck(d.exp, vtenv1, ftenv1)
        checkTypesEqual(t, d.opttype, d)
        vtenv1 = vtenv1 + (d.x -> d.opttype.getOrElse(t))
      }
      // We start by creating a function type environment with all the functions declared in the block
      for (d <- defs) {
        val (argType, returnType) = getFunType(d)
        ftenv1 = ftenv1 + (d.fun -> (argType, returnType))
      }
      for (d <- defs) {
        // we then create new variable type environment for type checking the parameters.
        // this shouldnt be saved, as it would leak the scope.
        var newVtenv = vtenv1
        val (argType, returnType) = getFunType(d)
        for ((a, p) <- argType.zip(d.params)) {
          newVtenv = newVtenv + (p.x -> a)
        }
        // We now type check the body against the return type. We have access to the types of any
        // functions invoked within.
        val bodyType = typeCheck(d.body, newVtenv, ftenv1)
        checkTypesEqual(bodyType, Some(returnType), d)
      }
      typeCheck(exp, vtenv1, ftenv1)
    case TupleExp(exps) => TupleType(exps.map(exp => typeCheck(exp, vtenv, ftenv)))
    case MatchExp(exp, cases) =>
      val exptype = typeCheck(exp, vtenv, ftenv)
      exptype match {
        case TupleType(ts) =>
          var res: Option[Type] = None
          for (c <- cases) {
            if (ts.length == c.pattern.length) {
              var newVtenv = vtenv
              for ((t, pat) <- ts.zip(c.pattern)) {
                newVtenv = newVtenv + (pat -> t)
              }
              val caseType = typeCheck(c.exp, newVtenv, ftenv)
              res match {
                case None => res = Some(caseType)
                case Some(t) =>
                  if (t != caseType) {
                    throw TypeError("case expressions should be of the same type...", e)
                  }
              }
              }
            }
          res match {
            case Some(t) => t
            case None => throw TypeError(s"No case matches type ${exptype}", e)
          }
        case _ => throw TypeError(s"Tuple expected at match, found ${exptype}", e)
      }
    case CallExp(fun, args) =>
      val (paramTypes, returnType) = ftenv.getOrElse(fun, throw TypeError("Function not declared", e))
      if (paramTypes.length != args.length) {
        throw TypeError("Incorrect number of arguments for function" ,e )
      }
      for ((a, p) <- args.zip(paramTypes)) {
        checkTypesEqual(typeCheck(a, vtenv, ftenv), Some(p), a)
      }
      returnType
  }

  /**
    * Returns the parameter types and return type for the function declaration `d`.
    */
  def getFunType(d: DefDecl): (List[Type], Type) =
    (d.params.map(p => p.opttype.getOrElse(throw TypeError(s"Type annotation missing at parameter ${p.x}", p))),
      d.optrestype.getOrElse(throw TypeError(s"Type annotation missing at function result ${d.fun}", d)))

  /**
    * Checks that the types `t1` and `ot2` are equal (if present), throws type error exception otherwise.
    */
  def checkTypesEqual(t1: Type, ot2: Option[Type], n: AstNode): Unit = ot2 match {
    case Some(t2) =>
      if (t1 != t2)
        throw TypeError(s"Type mismatch: expected type ${t2}, found type ${t1}", n)
    case None => // do nothing
  }

  /**
    * Builds an initial type environment, with a type for each free variable in the program.
    */
  def makeInitialVarTypeEnv(program: Exp): VarTypeEnv = {
    var vtenv: VarTypeEnv = Map()
    for (x <- Vars.freeVars(program))
      vtenv = vtenv + (x -> IntType())
    vtenv
  }

  /**
    * Exception thrown in case of MiniScala type errors.
    */
  class TypeError(msg: String, node: AstNode) extends MiniScalaError(s"Type error: $msg", node.pos)
}
