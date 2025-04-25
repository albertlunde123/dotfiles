package miniscala

import miniscala.Ast.*

/**
  * Interpreter for MiniScala.
  */
object Interpreter {

  def eval(e: Exp): Int = e match {
    case IntLit(c) =>
      trace(s"returning integer $c")
      c
    case BinOpExp(leftexp, op, rightexp) =>
      trace(s"evaluating binary operation $leftexp $op $rightexp")
      val leftval = eval(leftexp)
      val rightval = eval(rightexp)
      op match {
        case PlusBinOp() =>
          trace(s"adding $leftval and $rightval")
          leftval + rightval
        case MinusBinOp() =>
          trace(s"subtracting $leftval and $rightval")
          leftval - rightval
        case MultBinOp() =>
          trace(s"multiplying $leftval and $rightval")
          leftval * rightval
        case DivBinOp() =>
          trace(s"dividing $leftval by $rightval")
          if (rightval == 0)
            throw InterpreterError(s"Division by zero", op)
          leftval / rightval
        case ModuloBinOp() =>
          trace(s"taking $leftval modulo $rightval")
          leftval % rightval
        case MaxBinOp() =>
          trace(s"taking max of $leftval and $rightval")
          if (leftval > rightval) leftval else rightval
      }
    case UnOpExp(op, exp) =>
      val expval = eval(exp)
      op match {
        case NegUnOp() =>
          trace(s"negating $expval")
          -expval
      }
  }

  /**
    * Prints message if option -trace is used.
    */
  def trace(msg: String): Unit =
    if (Options.trace)
      println(msg)

  /**
    * Exception thrown in case of MiniScala runtime errors.
    */
  class InterpreterError(msg: String, node: AstNode) extends MiniScalaError(s"Runtime error: $msg", node.pos)
}
