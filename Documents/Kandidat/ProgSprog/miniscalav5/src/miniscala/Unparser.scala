package miniscala

import miniscala.Ast.*

/**
  * Unparser for MiniScala.
  */
object Unparser {

  /**
    * Unparse function.
    * Used for all kinds of AstNode objects, including Exp objects (see Ast.scala).
    */
  def unparse(n: AstNode): String = n match {
    case VarExp(x) => x
    case BinOpExp(leftexp, op, rightexp) =>
      val leftval = unparse(leftexp)
      val rightval = unparse(rightexp)
      op match {
        case PlusBinOp() => leftval + " + " + rightval
        case MinusBinOp() => leftval + " - " + rightval
        case MultBinOp() => leftval + " * " + rightval
        case DivBinOp() => leftval + " / " + rightval
        case EqualBinOp() => leftval + " == " + rightval
        case LessThanBinOp() => leftval + " < " + rightval
        case LessThanOrEqualBinOp() => leftval + " <= " + rightval
        case ModuloBinOp() => leftval + " % " + rightval
        case MaxBinOp() => s"max($leftval, $rightval)"
        case AndBinOp() => leftval + " && " + rightval
        case OrBinOp() => leftval + " || " + rightval
      }
    case UnOpExp(op, exp) =>
      val _exp = unparse(exp)
      op match {
        case NegUnOp() => s"-$_exp"
        case NotUnOp() => s"!$_exp"
      }
    case IfThenElseExp(condexp, thenexp, elseexp) =>
      val condval = unparse(condexp)
      val thenval = unparse(thenexp)
      val elseval = unparse(elseexp)
      s"if ($condval) $thenval else $elseval"
    case TupleExp(exps) =>
      var res = "("
      for (exp <- exps) {
        res = res + unparse(exp) + ", "
      }
      res.dropRight(2) + ")"
    case MatchCase(vars, exp) =>
      var res = "\tcase ("
      for (v <- vars) {
        res = res + v + ", "
      }
      res.dropRight(2) + ") => " + unparse(exp)
    case MatchExp(exp, cases) =>
      var res = unparse(exp) + " match {\n"
      for (_case <- cases) {
        res = res + unparse(_case) + "\n"
      }
      res + "}"
    case CallExp(fun, args) =>
      var res = s"$fun("
      for (arg <- args) {
        res = res + unparse(arg) + ", "
      }
      res.dropRight(2) + ")"
    case DefDecl(fun, params, optrestype, body) => 
      var res = s"def $fun("
      for (param <- params) {
        res = res + param.x + unparse(param.opttype) + ", "
      }
      res.dropRight(2) + ")" + unparse(optrestype) + " = " + unparse(body)
    case ValDecl(c, opttype, exp) =>
      "val " + c + unparse(opttype) + " = " + unparse(exp)
    case BlockExp(vals, defs, exp) => 
      var res = "{ "
      for (val_ <- vals) {
        res = res + unparse(val_) + "; "
      }
      for (def_ <- defs) {
        res = res + unparse(def_) + "; "
      }
      res + unparse(exp) + "}"
    case TupleType(types) =>
      var res = "("
      for (type_ <- types) {
        res = res + unparse(type_) + ", "
      }
      res.dropRight(2) + ")"
    case IntLit(c) => s"$c"
    case BoolLit(c) => s"$c"
    case FloatLit(c) => s"$c"
    case StringLit(c) => c
    case IntType() => "Int"
    case BoolType() => "Boolean"
    case FloatType() => "Float"
    case StringType() => "String"
  }

  /**
    * Unparse function for optional type annotations.
    */
  def unparse(ot: Option[Type]): String = ot match {
    case Some(t) => ": " + unparse(t)
    case None => ""
  }
}
