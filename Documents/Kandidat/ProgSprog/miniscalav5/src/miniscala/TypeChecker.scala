package miniscala

import miniscala.Ast.*
import miniscala.Unparser.unparse

/**
  * Type checker for MiniScala.
  */
object TypeChecker {

  type TypeEnv = Map[Id, Type]

  def typeCheck(e: Exp, tenv: TypeEnv): Type = e match {
    case IntLit(_) => IntType()
    case BoolLit(_) => BoolType()
    case FloatLit(_) => FloatType()
    case StringLit(_) => StringType()
    case VarExp(x) =>
      tenv.get(x) match {
        case Some(t) => t
        case None => throw TypeError("Undefined variable", VarExp(x))
      }
    case BinOpExp(leftexp, op, rightexp) =>
      val lefttype = typeCheck(leftexp, tenv)
      val righttype = typeCheck(rightexp, tenv)
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
            case _ => throw TypeError(s"Type mismatch at '+', unexpected types ${unparse(lefttype)} and ${unparse(righttype)}", op)
          }
        case MinusBinOp() | MultBinOp() | DivBinOp() | ModuloBinOp() | MaxBinOp() =>
          (lefttype, righttype) match {
            case (IntType(), IntType()) => IntType()
            case (FloatType(), FloatType()) => FloatType()
            case (IntType(), FloatType()) => FloatType()
            case (FloatType(), IntType()) => FloatType()
            case _ => throw TypeError(s"Type mismatch at $op unexpected types $lefttype and $righttype", op)
          }
        case EqualBinOp() => BoolType()
        case LessThanBinOp() | LessThanOrEqualBinOp() =>
          (lefttype, righttype) match {
            case (IntType(), IntType()) => BoolType()
            case (FloatType(), FloatType()) => BoolType()
            case (IntType(), FloatType()) => BoolType()
            case (FloatType(), IntType()) => BoolType()
            case _ => throw TypeError(s"Type mismatch at $op unexpected types $lefttype and $righttype", op)
          }
        case AndBinOp() | OrBinOp() =>
          (lefttype, righttype) match {
            case (BoolType(), BoolType()) => BoolType()
            case _ => throw TypeError(s"Type mismatch at $op unexpected types $lefttype and $righttype", op)
          }
      }
    case UnOpExp(op, exp) =>
      val exptype = typeCheck(exp, tenv)
      op match {
        case NegUnOp() =>
          exptype match {
            case IntType() | FloatType() => exptype
            case _ => throw TypeError(s"Cannot negate type $exptype", op)
          }
        case NotUnOp() =>
          exptype match {
            case BoolType() => exptype
            case _ => throw TypeError(s"Cannot perform logical NOT on non-boolean type $exptype", op)
          }
      }
    case IfThenElseExp(condexp, thenexp, elseexp) =>
      val condtype = typeCheck(condexp, tenv)
      if (condtype != BoolType()) {
        throw TypeError("condition should be boolean", condexp)
      }
      val thentype = typeCheck(thenexp, tenv)
      val elsetype = typeCheck(elseexp, tenv)
      if (thentype == elsetype) {
        thentype
      }
      else throw TypeError("then and else statement should be of the same type", e)
    case BlockExp(vals, defs, exp) =>
      var tenv1 = tenv
      for (d <- vals) {
        val t = typeCheck(d.exp, tenv1)
        checkTypesEqual(t, d.opttype, d)
        tenv1 = tenv1 + (d.x -> d.opttype.getOrElse(t))
      }
      for (d <- defs) {
        // d = def f(x_1 : t_1,...,x_m : t_m) : t = e
        val funtype = makeFunType(d)
        var tenv2 = tenv1
        for ((param, paramtype) <- d.params.zip(funtype.paramtypes)) {
          checkTypesEqual(paramtype, param.opttype, d)
          tenv2 = tenv2 + (param.x -> paramtype)
        } // tenv2 = tenv1[x_1 -> t_1,..., x_m -> t_m]
        val t = typeCheck(d.body, tenv2)
        checkTypesEqual(t, d.optrestype, d)
        tenv1 = tenv1 + (d.fun -> funtype)
      }
      typeCheck(e, tenv1)
    case TupleExp(exps) => TupleType(exps.map(exp => typeCheck(exp, tenv)))
    case MatchExp(exp, cases) =>
      val exptype = typeCheck(exp, tenv)
      exptype match {
        case TupleType(ts) => // exptype = (tau1, tau2)
          var res: Option[Type] = None
          for (c <- cases) {
            if (ts.length == c.pattern.length) { // ts=(tau1, tau2) and c.pattern=(x1, x2)
              var tenv1 = tenv
              for ((x, tau) <- c.pattern.zip(ts)) {
                tenv1 = tenv1 + (x -> tau)
              }
              val caseType = typeCheck(c.exp, tenv1)
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
            case None => throw TypeError(s"No case matches type ${unparse(exptype)}", e)
          }
        case _ => throw TypeError(s"Tuple expected at match, found ${unparse(exptype)}", e)
      }
    case CallExp(funexp, args) =>
      val funtype = typeCheck(funexp, tenv)
      funtype match {
        case FunType(paramtypes, restype) =>
          val n = paramtypes.length
          val m = args.length
          if (n == m) {
            args.zip(paramtypes).foreach(
              (arg, param) =>
              checkTypesEqual(typeCheck(arg, tenv), Some(param), e)
            )
            restype
          }
          else {
            throw TypeError(s"Function expects $n arguments but $m were given", e)
          }
        case _ => throw TypeError("Type of funexp must be FunType", e)
      }
    case LambdaExp(params, body) =>
      val tenv1 = tenv ++ params.map(
        param =>
        param.x -> param.opttype.getOrElse(
          throw TypeError(s"${param.x} has type-annotaion", e))
        )
      FunType(params.map(param => tenv1(param.x)), typeCheck(body, tenv1))
  }

  /**
    * Returns the function type for the function declaration `d`.
    */
  def makeFunType(d: DefDecl): FunType =
    FunType(d.params.map(p => p.opttype.getOrElse(throw TypeError(s"Type annotation missing at parameter ${p.x}", p))),
      d.optrestype.getOrElse(throw TypeError(s"Type annotation missing at function result ${d.fun}", d)))

  /**
    * Checks that the types `t1` and `ot2` are equal (if present), throws type error exception otherwise.
    */
  def checkTypesEqual(t1: Type, ot2: Option[Type], n: AstNode): Unit = ot2 match {
    case Some(t2) =>
      if (t1 != t2)
        throw TypeError(s"Type mismatch: expected type ${unparse(t2)}, found type ${unparse(t1)}", n)
    case None => // do nothing
  }

  /**
    * Builds an initial type environment, with a type for each free variable in the program.
    */
  def makeInitialTypeEnv(program: Exp): TypeEnv = {
    var tenv: TypeEnv = Map()
    for (x <- Vars.freeVars(program))
      tenv = tenv + (x -> IntType())
    tenv
  }

  /**
    * Exception thrown in case of MiniScala type errors.
    */
  class TypeError(msg: String, node: AstNode) extends MiniScalaError(s"Type error: $msg", node.pos)
}
