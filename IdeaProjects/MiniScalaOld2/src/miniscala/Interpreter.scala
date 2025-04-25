package miniscala

import miniscala.Ast.*

import scala.io.StdIn

/**
  * Interpreter for MiniScala.
  */
object Interpreter {

  type VarEnv = Map[Var, Int]

  def eval(e: Exp, venv: VarEnv): Int = e match {
    case IntLit(c) =>
      trace(s"returning integer $c")
      c
    case VarExp(x) => 
      trace(s"looking up variable $x")
      venv(x)
    case BinOpExp(leftexp, op, rightexp) =>
      trace(s"evaluating binary operation $leftexp $op $rightexp")
      val leftval = eval(leftexp, venv)
      
      val rightval = eval(rightexp, venv)
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
      val expval = eval(exp,venv)
      op match {
        case NegUnOp() =>
          trace(s"negating $expval")
          -expval
      }
    case BlockExp(vals, exp) =>
      trace("evaluating the block")
      var venv1 = venv
      for (d <- vals) {
        trace(s"assigning ${d.x} to ${d.exp}")
        venv1 = venv1 + (d.x -> eval(d.exp, venv1))
      }
      eval(exp, venv1)
  }

  /**
    * Builds an initial environment, with a value for each free variable in the program.
    */
  def makeInitialVarEnv(program: Exp): VarEnv = {
    var venv = Map[Var, Int]()
    for (x <- Vars.freeVars(program)) {
      print(s"Please provide an integer value for the variable $x: ")
      venv = venv + (x -> StdIn.readInt())
    }
    venv
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
