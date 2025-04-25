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
    case BoolLit(_) => ???
    case FloatLit(_) => ???
    case StringLit(_) => ???
    case VarExp(x) => ???
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
            case _ => throw TypeError(s"Type mismatch at '+', unexpected types ${unparse(lefttype)} and ${unparse(righttype)}", op)
          }
        case MinusBinOp() | MultBinOp() | DivBinOp() | ModuloBinOp() | MaxBinOp() => ???
        case EqualBinOp() => ???
        case LessThanBinOp() | LessThanOrEqualBinOp() => ???
        case AndBinOp() | OrBinOp() => ???
      }
    case UnOpExp(op, exp) => ???
    case IfThenElseExp(condexp, thenexp, elseexp) => ???
    case BlockExp(vals, defs, exp) =>
      var tenv = (vtenv, ftenv)
      for (d <- vals) {
        val t = typeCheck(d.exp, tenv._1, tenv._2)
        checkTypesEqual(t, d.opttype, d)
        tenv = (tenv._1 + (d.x -> d.opttype.getOrElse(t)), tenv._2)
      }
      ???
    case TupleExp(exps) => TupleType(???)
    case MatchExp(exp, cases) =>
      val exptype = typeCheck(exp, vtenv, ftenv)
      exptype match {
        case TupleType(ts) =>
          var res: Option[Type] = None
          for (c <- cases) {
            if (ts.length == c.pattern.length) {
              ???
            }
          }
          res match {
            case Some(t) => t
            case None => throw TypeError(s"No case matches type ${unparse(exptype)}", e)
          }
        case _ => throw TypeError(s"Tuple expected at match, found ${unparse(exptype)}", e)
      }
    case CallExp(fun, args) =>
      ???
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
        throw TypeError(s"Type mismatch: expected type ${unparse(t2)}, found type ${unparse(t1)}", n)
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
