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
  class ClosureVal(val params: List[FunParam],
                   val optrestype: Option[Type],
                   val body: Exp,
                   var env: Env) extends Val

  object ClosureVal {
    def apply(params: List[FunParam], optrestype: Option[Type], body: Exp, env: Env) =
      new ClosureVal(params, optrestype, body, env)

    def unapply(cl: ClosureVal): Option[(List[FunParam], Option[Type], Exp, Env)] =
      Some((cl.params, cl.optrestype, cl.body, cl.env))
  }

  case class RefVal(loc: Loc, opttype: Option[Type]) extends Val

  val unitVal: Val = TupleVal(Nil)
  type Env = Map[Id, Val]

  val sto = new scala.collection.mutable.ArrayBuffer[Val]
  type Loc = Int


  /**
    * Evaluates an expression.
    */
  def eval(e: Exp, env: Env): Val = e match {
    case IntLit(c) => IntVal(c)
    case BoolLit(c) => BoolVal(c)
    case FloatLit(c) => FloatVal(c)
    case StringLit(c) => StringVal(c)
    case VarExp(x) =>
      env.getOrElse(x, throw InterpreterError(s"Unknown identifier '$x'", e)) match {
        case RefVal(loc, _) => sto(loc)
        case v: Val => v
      }
    case BinOpExp(leftexp, op, rightexp) =>
      val leftval = eval(leftexp, env)
      val rightval = eval(rightexp, env)
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
      val expval = eval(exp, env)
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
      val condval = eval(condexp, env)
      condval match {
        case BoolVal(v) => if (v) eval(thenexp, env) else eval(elseexp, env)
        case _ => throw InterpreterError(s"Type mismatch at 'IfThenElse', unexpected value ${valueToString(condval)}", condexp)
    }
    case b @ BlockExp(vals, vars, defs, exps) =>
      var env1 = env
      for (d <- vals ++ vars ++ defs) {
        val env2 = eval(d, env1, b)
        env1 = env2
      }
      for (d <- defs) {
        env1(d.fun) match {
          case c: ClosureVal => c.env = env1
        }
      }
      var v1 = unitVal
      for (e <- exps) {
        val v2 = eval(e, env1)
        v1 = v2
      }
      v1
    case TupleExp(exps) =>
      var vals = List[Val]()
      for (exp <- exps) {
        val v = eval(exp, env)
        vals = v :: vals
      }
      TupleVal(vals.reverse)
    case MatchExp(exp, cases) =>
      val expval = eval(exp, env)
      expval match {
        case TupleVal(vs) =>
          var res: Option[Val] = None
          for (c <- cases) {
            if (vs.length == c.pattern.length) {
              var newEnv: Env = env
              val zs = vs.zip(c.pattern)
              for ((v, c) <- zs) {
                newEnv = newEnv + (c -> v)
              }
              res = Some(eval(c.exp, newEnv))
            }
          }
          res match {
            case Some(v) => v
            case None => throw InterpreterError(s"No case matches value ${valueToString(expval)}", e)
          }
        case _ => throw InterpreterError(s"Tuple expected at match, found ${valueToString(expval)}", e)
      }
    case CallExp(funexp, args) =>
      // We can expect funexp to be a variable VarExp or a LambdaExp
      // Evaluating either of these will give a ClosureVal, in the lambda case optrestype = None and
      // defs is an empty list. But as they are still ClosureVal, we can just evaluate them.
      val funVal = eval(funexp, env)
      val closure = funVal match {
        case ClosureVal(params, optrestype, body, env) =>
          if (params.length != args.length) throw InterpreterError("incorrect number of arguments", e)
          ClosureVal(params, optrestype, body, env)
        case _ => throw InterpreterError(s"Unknown function ${funexp}", e)
      }
      var newEnv = closure.env
      for ((arg, pm) <- args.zip(closure.params)) {
        val accVal = eval(arg, env)
        checkValueType(accVal, pm.opttype, e)
        newEnv = newEnv + (pm.x -> accVal)
      }
      //for (d <- closure.defs) {
      //  newEnv = newEnv + (d.fun -> ClosureVal(d.params, d.optrestype, d.body, newEnv, closure.defs))
      //}
      val ret = eval(closure.body, newEnv)
      checkValueType(ret, closure.optrestype, e)
      ret

    case LambdaExp(params, body) =>
      ClosureVal(params, None, body, env)

    case AssignmentExp(x, exp) =>
      val v1 = eval(exp, env)
      val (loc, t1) = env.getOrElse(x, throw InterpreterError(s"variable ${x} not declared", e)) match {
        case RefVal(loc,  t1) =>
          checkValueType(v1, t1, e)
          (loc, t1)
        case _ => throw InterpreterError("variable doesn't have a location", e)
      }
      sto.update(loc, v1)
      unitVal

    case WhileExp(cond, body) =>
      val bool = eval(cond, env)
      bool match {
        case BoolVal(false) => unitVal
        case BoolVal(true) =>
          eval(body, env)
          eval(WhileExp(cond, body), env)
        case _ => throw InterpreterError("While-loop condition is not boolean", e)
      }
  }

  /**
    * Evaluates a declaration.
    */
  def eval(d: Decl, env: Env, b: BlockExp): Env = d match {
    case ValDecl(x, opttype, exp) =>
      val v = eval(exp, env)
      checkValueType(v, opttype, exp)
      val env1 = env + (x -> v)
      env1

    case VarDecl(x, opttype, exp) =>
      val v = eval(exp, env)
      checkValueType(v, opttype, exp)
      val l = sto.length
      val env1 = env + (x -> RefVal(l, opttype))
      sto += v
      env1

    case DefDecl(fun, params, optrestype, body) =>
      val closure = ClosureVal(params, optrestype, body, env)
      env + (fun -> closure)
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
        case (ClosureVal(cparams, optcrestype, _, _), FunType(paramtypes, restype)) if cparams.length == paramtypes.length =>
          for ((p, t) <- cparams.zip(paramtypes))
            checkTypesEqual(t, p.opttype, n)
          checkTypesEqual(restype, optcrestype, n)
        case _ =>
          throw InterpreterError(s"Type mismatch: value ${valueToString(v)} does not match type ${unparse(t)}", n)
      }
    case None => // do nothing
  }

  /**
    * Checks that the types `t1` and `ot2` are equal (if present), throws type error exception otherwise.
    */
  def checkTypesEqual(t1: Type, ot2: Option[Type], n: AstNode): Unit = ot2 match {
    case Some(t2) =>
      if (t1 != t2)
        throw InterpreterError(s"Type mismatch: type ${unparse(t1)} does not match type ${unparse(t2)}", n)
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
    case ClosureVal(params, _, exp, _) => // the resulting string ignores the result type annotation and the declaration environment
      s"<(${params.map(unparse).mkString(",")}), ${unparse(exp)}>"
    case RefVal(loc, _) => s"#$loc" // the resulting string ignores the type annotation
  }

  /**
    * Builds an initial environment, with a value for each free variable in the program.
    */
  def makeInitialEnv(program: Exp): Env = {
    var env = Map[Id, Val]()
    for (x <- Vars.freeVars(program)) {
      print(s"Please provide an integer value for the variable $x: ")
      env = env + (x -> IntVal(StdIn.readInt()))
    }
    env
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
