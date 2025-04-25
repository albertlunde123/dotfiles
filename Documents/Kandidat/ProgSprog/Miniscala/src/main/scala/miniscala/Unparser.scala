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
    // VarExp expressions just need to return the variable as a string.
    case VarExp(x) => s"${x}"
    case ValDecl(x, exp) => s"val ${x}" + " = " + unparse(exp) + "; "
    case BlockExp(lists, rightexp) =>
      val rightval = unparse(rightexp)
      def unparseList(list: List[ValDecl]): String = list match {
        // matches on any list(c1, ..., cn) if n>=1
        case c :: cs => unparse(c) + unparseList(cs)
        // handles the case where cs was the empty list
        case Nil => ""
      }
      val list = unparseList(lists)
      "{" + list + rightval + "}"
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
      }
    case UnOpExp(op, exp) =>
        val expval = unparse(exp)
        op match {
            case NegUnOp() => s"-${expval}"
      }
  }
}
