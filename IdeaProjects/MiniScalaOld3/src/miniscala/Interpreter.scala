package miniscala

import miniscala.Ast.*
import miniscala.Unparser.unparse

import scala.io.StdIn

/**
  * Interpreter for MiniScala.
  */
object Interpreter {

  sealed abstract class Val
  case class IntVal(v: Int) extends Val
  case class BoolVal(v: Boolean) extends Val
  case class FloatVal(v: Float) extends Val
  case class StringVal(v: String) extends Val
  case class TupleVal(vs: List[Val]) extends Val

  type VarEnv = Map[Var, Val]

  def eval(e: Exp, venv: VarEnv): Val = e match {
    case IntLit(c) => IntVal(c)
    case BoolLit(c) => BoolVal(c)
    case FloatLit(c) => FloatVal(c)
    case StringLit(c) => StringVal(c)
    case VarExp(x) =>
      venv.getOrElse(x, throw InterpreterError(s"Unknown identifier '$x'", e))
    case BinOpExp(leftexp, op, rightexp) =>
      val leftval = eval(leftexp, venv)
      val rightval = eval(rightexp, venv)
      op match {
        case PlusBinOp() =>
          (leftval, rightval) match {
            case (IntVal(v1), IntVal(v2)) => IntVal(v1 + v2)
            case (FloatVal(v1), FloatVal(v2)) => FloatVal(v1 + v2)
            case (IntVal(v1), FloatVal(v2)) => FloatVal(v1 + v2)
            case (FloatVal(v1), IntVal(v2)) => FloatVal(v1 + v2)
            case (StringVal(v1), StringVal(v2)) => StringVal(v1 + v2)
            case (StringVal(v1), IntVal(v2)) => StringVal(v1 + v2.toString)
            case (StringVal(v1), FloatVal(v2)) => StringVal(v1 + v2.toString)
            case (IntVal(v1), StringVal(v2)) => StringVal(v1.toString + v2)
            case (FloatVal(v1), StringVal(v2)) => StringVal(v1.toString + v2)
            case _ => throw InterpreterError(s"Type mismatch at '+', unexpected values ${valueToString(leftval)} and ${valueToString(rightval)}", op)
          }
        case MinusBinOp() =>
          (leftval, rightval) match {
            case (IntVal(v1), IntVal(v2)) => IntVal(v1 - v2)
            case (FloatVal(v1), FloatVal(v2)) => FloatVal(v1 - v2)
            case (IntVal(v1), FloatVal(v2)) => FloatVal(v1 - v2)
            case (FloatVal(v1), IntVal(v2)) => FloatVal(v1 - v2)
            case _ => throw InterpreterError(s"Type mismatch at '-', unexpected values ${valueToString(leftval)} and ${valueToString(rightval)}", op)
          }
        case MultBinOp() =>
          (leftval, rightval) match {
            case (IntVal(v1), IntVal(v2)) => IntVal(v1 * v2)
            case (FloatVal(v1), FloatVal(v2)) => FloatVal(v1 * v2)
            case (IntVal(v1), FloatVal(v2)) => FloatVal(v1 * v2)
            case (FloatVal(v1), IntVal(v2)) => FloatVal(v1 * v2)
            case _ => throw InterpreterError(s"Type mismatch at '*', unexpected values ${valueToString(leftval)} and ${valueToString(rightval)}", op)
          }
        case DivBinOp() =>
          if (rightval == IntVal(0) || rightval == FloatVal(0.0f))
            throw InterpreterError(s"Division by zero", op)
          (leftval, rightval) match {
            case (IntVal(v1), IntVal(v2)) => IntVal(v1 / v2)
            case (FloatVal(v1), FloatVal(v2)) => FloatVal(v1 / v2)
            case (IntVal(v1), FloatVal(v2)) => FloatVal(v1 / v2)
            case (FloatVal(v1), IntVal(v2)) => FloatVal(v1 / v2)
            case _ => throw InterpreterError(s"Type mismatch at '/', unexpected values ${valueToString(leftval)} and ${valueToString(rightval)}", op)
          }
        case ModuloBinOp() =>
          if (rightval == IntVal(0) || rightval == FloatVal(0.0f))
            throw InterpreterError(s"modulo by zero", op)
          (leftval, rightval) match {
            case (IntVal(v1), IntVal(v2)) => IntVal(v1 % v2)
            case (FloatVal(v1), FloatVal(v2)) => FloatVal(v1 % v2)
            case (IntVal(v1), FloatVal(v2)) => FloatVal(v1 % v2)
            case (FloatVal(v1), IntVal(v2)) => FloatVal(v1 % v2)
            case _ => throw InterpreterError(s"Type mismatch at '%', unexpected values ${valueToString(leftval)} and ${valueToString(rightval)}", op)
          }
        case EqualBinOp() =>
          def CheckEquals(val1: Val, val2: Val): BoolVal = (val1, val2) match {
            case (BoolVal(v1), BoolVal(v2)) => if (v1 == v2) BoolVal(true) else BoolVal(false)
            case (IntVal(v1), IntVal(v2)) => if (v1 == v2) BoolVal(true) else BoolVal(false)
            case (FloatVal(v1), FloatVal(v2)) => if (v1 == v2) BoolVal(true) else BoolVal(false)
            case (IntVal(v1), FloatVal(v2)) => if (v1 == v2) BoolVal(true) else BoolVal(false)
            case (FloatVal(v1), IntVal(v2)) => if (v1 == v2) BoolVal(true) else BoolVal(false)
            case (StringVal(v1), StringVal(v2)) => if (v1 == v2) BoolVal(true) else BoolVal(false)
            case _ => throw InterpreterError(s"Type mismatch at '==', unexpected values ${valueToString(leftval)} and ${valueToString(rightval)}", op)
          }
          (leftval, rightval) match {
            case (TupleVal(v1), TupleVal(v2)) =>
              if (v1.length != v2.length) {
                throw InterpreterError(s"Tuples are different length", op)
              }
              var allEqual = true
              val zs = v1.zip(v2)
              for ((u1, u2) <- zs) {
                if (!CheckEquals(u1, u2).v) {
                  allEqual = false
                }
              }
              BoolVal(allEqual)
            case (a, b) => CheckEquals(a, b)
          }
        case LessThanBinOp() => 
          (leftval, rightval) match {
            case (IntVal(v1), IntVal(v2)) => if (v1 < v2) BoolVal(true) else BoolVal(false)
            case (FloatVal(v1), FloatVal(v2)) => if (v1 < v2) BoolVal(true) else BoolVal(false)
            case (IntVal(v1), FloatVal(v2)) => if (v1 < v2) BoolVal(true) else BoolVal(false)
            case (FloatVal(v1), IntVal(v2)) => if (v1 < v2) BoolVal(true) else BoolVal(false)
            case _ => throw InterpreterError(s"Type mismatch at '<', unexpected values ${valueToString(leftval)} and ${valueToString(rightval)}", op)
          }
        case LessThanOrEqualBinOp() =>
          (leftval, rightval) match {
            case (IntVal(v1), IntVal(v2)) => if (v1 <= v2) BoolVal(true) else BoolVal(false)
            case (FloatVal(v1), FloatVal(v2)) => if (v1 <= v2) BoolVal(true) else BoolVal(false)
            case (IntVal(v1), FloatVal(v2)) => if (v1 <= v2) BoolVal(true) else BoolVal(false)
            case (FloatVal(v1), IntVal(v2)) => if (v1 <= v2) BoolVal(true) else BoolVal(false)
            case _ => throw InterpreterError(s"Type mismatch at '<=', unexpected values ${valueToString(leftval)} and ${valueToString(rightval)}", op)
          }
        case MaxBinOp() => 
          (leftval, rightval) match {
            case (IntVal(v1), IntVal(v2)) => IntVal(v1 max v2)
            case (FloatVal(v1), FloatVal(v2)) => FloatVal(v1 max v2)
            case (IntVal(v1), FloatVal(v2)) => FloatVal(v2 max v1)
            case (FloatVal(v1), IntVal(v2)) => FloatVal(v1 max v2)
            case _ => throw InterpreterError(s"Type mismatch at 'max', unexpected values ${valueToString(leftval)} and ${valueToString(rightval)}", op)
          }
        case AndBinOp() => 
          (leftval, rightval) match {
            case(BoolVal(v1), BoolVal(v2)) => if (v1 & v2) BoolVal(true) else BoolVal(false)
            case _ => throw InterpreterError(s"Type mismatch at 'and', unexpected values ${valueToString(leftval)} and ${valueToString(rightval)}", op)
        }
        case OrBinOp() => 
          (leftval, rightval) match {
            case(BoolVal(v1), BoolVal(v2)) => if (v1 | v2) BoolVal(true) else BoolVal(false)
            case _ => throw InterpreterError(s"Type mismatch at 'and', unexpected values ${valueToString(leftval)} and ${valueToString(rightval)}", op)
        }
      }
    case UnOpExp(op, exp) =>
      val expval = eval(exp, venv)
      op match {
        case NegUnOp() =>
          expval match {
            case IntVal(v) => IntVal(-v)
            case FloatVal(v) => FloatVal(-v)
            case _ => throw InterpreterError(s"Type mismatch at '-', unexpected value ${valueToString(expval)}", op)
          }
        case NotUnOp() =>
          expval match {
            case BoolVal(v) => if (v) BoolVal(false) else BoolVal(true)
            case _ => throw InterpreterError(s"Type mismatch at '!', unexpected value ${valueToString(expval)}", op)
          }
      }
    case IfThenElseExp(condexp, thenexp, elseexp) => 
      val condval = eval(condexp, venv)
      val thenval = eval(thenexp, venv)
      val elseval = eval(elseexp, venv)
      condval match {
        case BoolVal(v) => if (v) thenval else elseval
        case _ => throw InterpreterError(s"Type mismatch at 'IfThenElse', unexpected value ${valueToString(condval)}", condexp)
    }
    case BlockExp(vals, exp) =>
      var venv1 = venv
      for (d <- vals) {
        val value = eval(d.exp, venv1)
        checkValueType(value, d.opttype, d)
        venv1 = venv1 + (d.x -> eval(d.exp, venv1))
      }
      eval(exp, venv1)
    case TupleExp(exps) =>
      var vals = List[Val]()
      for (exp <- exps)
        vals = eval(exp, venv) :: vals
      TupleVal(vals.reverse)
    case MatchExp(exp, cases) =>
      val expval = eval(exp, venv)
      expval match {
        case TupleVal(vs) =>
          var res: Option[Val] = None
          for (c <- cases) {
            if (vs.length == c.pattern.length && res.isEmpty) {
              var newVenv: VarEnv = venv
              val zs = vs.zip(c.pattern)
              for ((v, c) <- zs) {
                newVenv = newVenv + (c -> v)
              }
              res = Some(eval(c.exp, newVenv))
            }
          }
          res match {
            case Some(v) => v
            case None => throw InterpreterError(s"No case matches value ${valueToString(expval)}", e)
          }
        case _ => throw InterpreterError(s"Tuple expected at match, found ${valueToString(expval)}", e)
      }
  }

  /**
    * Checks whether value `v` has type `ot` (if present), generates runtime type error otherwise.
    */
  def checkValueType(v: Val, ot: Option[Type], n: AstNode): Unit = ot match {
    case Some(t) =>
      (v, t) match {
        case (IntVal(_), IntType()) |
             (BoolVal(_), BoolType()) |
             (FloatVal(_), FloatType()) |
             (IntVal(_), FloatType()) |
             (StringVal(_), StringType()) => // do nothing
        case (TupleVal(vs), TupleType(ts)) if vs.length == ts.length =>
          for ((vi, ti) <- vs.zip(ts))
            checkValueType(vi, Some(ti), n)
        case _ =>
          throw InterpreterError(s"Type mismatch: value ${valueToString(v)} does not match type $t}", n)
      }
    case None => // do nothing
  }

  /**
    * Converts a value to its string representation (for error messages).
    */
  def valueToString(v: Val): String = v match {
    case IntVal(c) => c.toString
    case FloatVal(c) => c.toString
    case BoolVal(c) => c.toString
    case StringVal(c) => c
    case TupleVal(vs) => vs.map(valueToString).mkString("(", ",", ")")
  }

  /**
    * Builds an initial environment, with a value for each free variable in the program.
    */
  def makeInitialVarEnv(program: Exp): VarEnv = {
    var venv = Map[Var, Val]()
    for (x <- Vars.freeVars(program)) {
      print(s"Please provide an integer value for the variable $x: ")
      venv = venv + (x -> IntVal(StdIn.readInt()))
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
