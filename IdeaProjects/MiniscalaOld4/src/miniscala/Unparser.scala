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
    case IntLit(c) => s"${c}"
    case BoolLit(c) => s"${c}"
    // VarExp expressions just need to return the variable as a string.
    case VarExp(x) => s"${x}"
    case ValDecl(x, opt,  exp) => s"val ${x}" + unparse(opt) + " = " + unparse(exp) + "; "
    case FunParam(x, opttype) => s"${x}: " + unparse(opttype)
    case DefDecl(fun, params, opt, exp) =>
      val f = s"${fun}"
      val body = unparse(exp)
      var pms = ""
      val types = unparse(opt)
      for (p <- params) {
        pms = pms + unparse(p)
      }
      f + "(" + pms + ")" + types + " = " + body + "; "
    case CallExp(fun, params) =>
      val f = s"${fun}"
      var pms = ""
      for (p <- params) {
        pms = pms + unparse(p)
      }
      f + "(" + pms + ")"
    case BlockExp(vals, defs, rightexp) =>
      val rightval = unparse(rightexp)
      def unparseListDef(list: List[DefDecl]): String = list match {
        case c :: cs =>
          println("hello")
          unparse(c) + unparseListDef(cs)
        // handles the case where cs was the empty list
        case Nil => ""
      }
      def unparseListVal(list: List[ValDecl]): String = list match {
        // matches on any list(c1, ..., cn) if n>=1
        case c :: cs => unparse(c) + unparseListVal(cs)
        // handles the case where cs was the empty list
        case Nil => ""
      }
      val valsup = unparseListVal(vals)
      val defsup = unparseListDef(defs)
      println(defsup)
      "{" + valsup + defsup + rightval + "}"
    case BinOpExp(leftexp, op, rightexp) =>
      val leftval = unparse(leftexp)
      val rightval = unparse(rightexp)
      op match {
        case PlusBinOp() => s"${leftval} + ${rightval}"
        case MinusBinOp() => s"${leftval} - ${rightval}"
        case MultBinOp() => s"${leftval} * ${rightval}"
        case DivBinOp() => s"${leftval} / ${rightval}"
        case ModuloBinOp() => s"${leftval} % ${rightval}"
        case MaxBinOp() => s"${leftval} max ${rightval}"
        case EqualBinOp() => s"${leftval} == ${rightval}"
        case LessThanBinOp() => s"${leftval} < ${rightval}"
        case LessThanOrEqualBinOp() => s"${leftval} <= ${rightval}"
        case AndBinOp() => s"${leftval} & ${rightval}"
        case OrBinOp() => s"${leftval} | ${rightval}"
      }
    case UnOpExp(op, exp) =>
      val expval = unparse(exp)
      op match {
        case NegUnOp() => s"-${expval}"
        case NotUnOp() => s"!${expval}"
      }
    case IfThenElseExp(condexp, thenexp, elseexp) => 
      val condval = unparse(condexp)
      val thenval = unparse(thenexp)
      val elseval = unparse(elseexp)
      "if (${condval}) ${thenval} else ${elseval}"
    case TupleExp(exps) =>
      var exp = ""
      for (e <- exps) {
        exp = exp + unparse(e) + ", "
      }
      "(" + exp.dropRight(2) + ")"
     case MatchCase(vars, exp) =>
       val exps = unparse(exp)
       var vs = ""
       for (v <- vars) {
         vs = vs + s"${v}" + ", "
       }
      "    case (" + vs.dropRight(2) + ")" + " => " + exps
    case MatchExp(exp, matchcases) =>
      val exps = unparse(exp)
      var mcs = ""
      for (m <- matchcases) {
        mcs = mcs + unparse(m) + "\n"
      }
      exps + " match {\n" + mcs + "}"
    case IntType() => "Int"
    case BoolType() => "Boolean"
    case StringType() => "String"
    case FloatType() => "Float"
    case TupleType(types_list) =>
      var typ = ""
      for (t <- types_list) {
        typ = typ + unparse(t) + ", "
      }
      "(" + typ.dropRight(2) + ")"
  }

  /**
    * Unparse function for optional type annotations.
    */
  def unparse(ot: Option[Type]): String = ot match {
    case Some(t) => ": " + unparse(t)
    case None => ""
  }
}
