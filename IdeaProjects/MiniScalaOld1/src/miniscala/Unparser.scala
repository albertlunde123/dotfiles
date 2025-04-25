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
    case BinOpExp(leftexp, op, rightexp) =>
      val leftval = unparse(leftexp)
      val rightval = unparse(rightexp)
      op match {
        case PlusBinOp() =>
          s"${leftval}+${rightval}"
        case MinusBinOp() =>
          s"${leftval}-${rightval}"
        case MultBinOp() =>
          s"${leftval}*${rightval}"
        case DivBinOp() =>
            s"${leftval}/${rightval}"
        case ModuloBinOp() =>
            s"${leftval}%${rightval}"
        case MaxBinOp() =>
            s"${leftval}max${rightval}"
      }
    case UnOpExp(op, exp) =>
        val expval = unparse(exp)
        op match {
            case NegUnOp() =>
                s"-${expval}"
      }
  }
}
