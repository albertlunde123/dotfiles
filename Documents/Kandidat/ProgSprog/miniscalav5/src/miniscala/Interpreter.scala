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
  case class ClosureVal(params: List[FunParam], optrestype: Option[Type], body: Exp, env: Env, defs: List[DefDecl]) extends Val

  type Env = Map[Id, Val]

  /**
    * Evaluates an expression.
    */
  def eval(e: Exp, env: Env): Val = e match {
    case IntLit(c) =>
      trace(s"Evaluating a integer literal $c")
      IntVal(c)
    case BoolLit(c) =>
      trace(s"Evaluating a boolean literal $c")
      BoolVal(c)
    case FloatLit(c) =>
      trace(s"Evaluating a float literal $c")
      FloatVal(c)
    case StringLit(c) =>
      trace(s"Evaluating a string literal $c")
      StringVal(c)
    case VarExp(x) =>
      val y = env.getOrElse(x, throw InterpreterError(s"Unknown identifier '$x'", e))
      trace(s"Associating $x with the value $y")
      y
    case BinOpExp(leftexp, op, rightexp) =>
      val leftval = eval(leftexp, env)
      trace(s"Evaluating the left-hand side ${valueToString(leftval)} of a binary operator expression $op")
      val rightval = eval(rightexp, env)
      trace(s"Evaluating the right-hand side ${valueToString(rightval)} of a binary operator expression $op")
      op match {
        case PlusBinOp() =>
          trace(s"Adding ${valueToString(leftval)} and ${valueToString(rightval)}")
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
          trace(s"Subtracting ${valueToString(rightval)} from ${valueToString(leftval)}")
          (leftval, rightval) match {
            case (IntVal(v1), IntVal(v2)) =>
              IntVal(v1 - v2)
            case (FloatVal(v1), FloatVal(v2)) =>
              FloatVal(v1 - v2)
            case (IntVal(v1), FloatVal(v2)) =>
              FloatVal(v1 - v2)
            case (FloatVal(v1), IntVal(v2)) =>
              FloatVal(v1 - v2)
            case _ => throw InterpreterError(s"Type mismatch at '-', unexpected values ${valueToString(leftval)} and ${valueToString(rightval)}", op)
          }
        case MultBinOp() =>
          trace(s"Multiplying ${valueToString(leftval)} and ${valueToString(rightval)}")
          (leftval, rightval) match {
            case (IntVal(v1), IntVal(v2)) =>
              IntVal(v1 * v2)
            case (FloatVal(v1), FloatVal(v2)) =>
              FloatVal(v1 * v2)
            case (IntVal(v1), FloatVal(v2)) =>
              FloatVal(v1 * v2)
            case (FloatVal(v1), IntVal(v2)) =>
              FloatVal(v1 * v2)
            case _ => throw InterpreterError(s"Type mismatch at '*', unexpected values ${valueToString(leftval)} and ${valueToString(rightval)}", op)
          }
        case DivBinOp() =>
          trace(s"Dividing ${valueToString(leftval)} with ${valueToString(rightval)}")
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
          trace(s"Calculating ${valueToString(leftval)} (mod ${valueToString(rightval)})")
          (leftval, rightval) match {
            case (IntVal(v1), IntVal(v2)) =>
              IntVal(v1 % v2)
            case (FloatVal(v1), FloatVal(v2)) =>
              FloatVal(v1 % v2)
            case (FloatVal(v1), IntVal(v2)) =>
              FloatVal(v1 % v2)
            case _ => throw InterpreterError(s"Type mismatch at '%', unexpected values ${valueToString(leftval)} and ${valueToString(rightval)}", op)
          }
        case EqualBinOp() =>
          trace(s"Assessing if ${valueToString(leftval)} == ${valueToString(rightval)}")
          var res = true
          def checkequal(val1: Val, val2: Val): BoolVal = (val1, val2) match {
            case (IntVal(v1), IntVal(v2)) => BoolVal(v1 == v2)
            case (FloatVal(v1), FloatVal(v2)) => BoolVal(v1 == v2)
            case (StringVal(v1), StringVal(v2)) => BoolVal(v1 == v2)
            case _ => throw InterpreterError(s"Type mismatch at '==', unexpected values ${valueToString(val1)} and ${valueToString(val2)}", op)
          }
          (leftval, rightval) match {
            case (TupleVal(v1), TupleVal(v2)) =>
              trace(s"Assessing if two tuples $v1 and $v2 are equal")
              if (v1.length != v2.length) {
                throw InterpreterError(s"Tuples are different length, cannot assess equality", op)
              }
              else {
                for ((w1, w2) <- v1.zip(v2)) {
                  res = checkequal(w1, w2).v
                }
              }
            case (v1, v2) =>
              trace(s"Assessing if two non-tuples $v1 and $v2 are equal")
              res = checkequal(v1, v2).v
          }
          BoolVal(res)
        case LessThanBinOp() =>
          trace(s"Assessing if ${valueToString(leftval)} < ${valueToString(rightval)}")
          (leftval, rightval) match {
            case (IntVal(v1), IntVal(v2)) =>
              BoolVal(v1 < v2)
            case (FloatVal(v1), FloatVal(v2)) =>
              BoolVal(v1 < v2)
            case (IntVal(v1), FloatVal(v2)) =>
              BoolVal(v1 < v2)
            case (FloatVal(v1), IntVal(v2)) =>
              BoolVal(v1 < v2)
            case _ => throw InterpreterError(s"Type mismatch at '<', unexpected values ${valueToString(leftval)} and ${valueToString(rightval)}", op)
          }
        case LessThanOrEqualBinOp() =>
          trace(s"Assessing if ${valueToString(leftval)} <= ${valueToString(rightval)}")
          (leftval, rightval) match {
            case (IntVal(v1), IntVal(v2)) =>
              BoolVal(v1 <= v2)
            case (FloatVal(v1), FloatVal(v2)) =>
              BoolVal(v1 <= v2)
            case (IntVal(v1), FloatVal(v2)) =>
              BoolVal(v1 <= v2)
            case (FloatVal(v1), IntVal(v2)) =>
              BoolVal(v1 <= v2)
            case _ => throw InterpreterError(s"Type mismatch at '<=', unexpected values ${valueToString(leftval)} and ${valueToString(rightval)}", op)
          }
        case MaxBinOp() =>
          trace(s"Determining max(${valueToString(leftval)}, ${valueToString(rightval)}")
          (leftval, rightval) match {
            case (IntVal(v1), IntVal(v2)) =>
              if (v1 <= v2) {
                IntVal(v2)
              }
              else {
                IntVal(v1)
              }
            case (FloatVal(v1), FloatVal(v2)) =>
              if (v1 <= v2) {
                FloatVal(v2)
              }
              else {
                FloatVal(v1)
              }
            case (IntVal(v1), FloatVal(v2)) =>
              if (v1 <= v2) {
                FloatVal(v2)
              }
              else {
                IntVal(v1)
              }
            case (FloatVal(v1), IntVal(v2)) =>
              if (v1 <= v2) {
                IntVal(v2)
              }
              else {
                FloatVal(v1)
              }
            case _ => throw InterpreterError(s"Type mismatch at 'max', unexpected values ${valueToString(leftval)} and ${valueToString(rightval)}", op)
          }
        case AndBinOp() =>
          (leftval, rightval) match {
            case (BoolVal(v1), BoolVal(v2)) =>
              trace(s"Determining if statement: $v1 AND $v2 is true")
              BoolVal(v1 && v2)
            case _ => throw InterpreterError(s"Type mismatch at 'AND', unexpected values ${valueToString(leftval)} and ${valueToString(rightval)}", op)
          }
        case OrBinOp() =>
          (leftval, rightval) match {
            case (BoolVal(v1), BoolVal(v2)) =>
              trace(s"Determining if statement: $v1 OR $v2 is true")
              BoolVal(v1 || v2)
            case _ => throw InterpreterError(s"Type mismatch at 'OR', unexpected values ${valueToString(leftval)} and ${valueToString(rightval)}", op)
          }
      }
    case UnOpExp(op, exp) =>
      val expval = eval(exp, env)
      op match {
        case NegUnOp() =>
          trace(s"Multiplying ${valueToString(expval)} by -1")
          expval match {
            case IntVal(v) => IntVal(-v)
            case FloatVal(v) => FloatVal(-v)
            case _ => throw InterpreterError(s"Type mismatch at '-', unexpected value ${valueToString(expval)}", op)
          }
        case NotUnOp() =>
          expval match {
            case BoolVal(v1) =>
              trace(s"Determining if statement NOT $v1 is true")
              BoolVal(!v1)
            case _ => throw InterpreterError(s"Type mismatch at 'NOT', unexpected value ${valueToString(expval)}", op)
          }
      }
    case IfThenElseExp(condexp, thenexp, elseexp) =>
      trace("Assessing a if-then-else block")
      val condval = eval(condexp, env)
      condval match {
        case BoolVal(v) =>
          if (v) {
            eval(thenexp, env)
          }
          else {
            eval(elseexp, env)
          }
        case _ => throw InterpreterError(s"Type mis-match at 'IfThenElse', ${valueToString(condval)} must be boolean", condexp)
      }
    case b @ BlockExp(vals, defs, exp) =>
      var env1 = env
      for (d <- vals ++ defs)
        env1 = eval(d, env1, b)
      eval(exp, env1)
    case TupleExp(exps) =>
      var vals = List[Val]()
      for (exp <- exps)
        vals = eval(exp, env) :: vals
      TupleVal(vals.reverse)
    case MatchExp(exp, cases) =>
      trace(s"Evaluating a match-expression")
      val expval = eval(exp, env)
      expval match {
        case TupleVal(vs) => // expval = (v1, v2)
          var res: Option[Val] = None
          for (c <- cases) {
            if (vs.length == c.pattern.length) { // vs=(v1, v2) and c.pattern=(x1, x2)
              var newEnv: Env = env
              val zs = vs.zip(c.pattern)
              for ((v, c) <- zs) {
                newEnv = newEnv + (c -> v)
              } // newEnv = env[x1 -> v1, x2 -> v2]
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
      val funval = eval(funexp, env)
      funval match {
        case ClosureVal(params, optrestype, body, env2, defs) =>
          // args = (e_1,...,e_n), params = (x_1,...,x_n)
          val n = params.length
          val m = args.length
          if (n == m) {
            val vals = args.map(e => eval(e, env)) // e_1 -> x_1,...,e_n -> x_n
            var env_ = env2
            for ((param, val_) <- params.zip(vals)) {
              checkValueType(val_, param.opttype, e) // For mutual recursion
              env_ = env_ + (param.x -> val_)
            } // env_ = env2[e_1 -> x_1,...,e_n -> x_n]
            for (d <- defs) {
              env_ = env_ + (d.fun -> ClosureVal(d.params, d.optrestype, d.body, env2, defs))
            } // env_ = env_[green-box on p. 17 `miniscala5`]
            val res = eval(body, env_)
            checkValueType(res, optrestype, e)
            res
          }
          else {
            throw InterpreterError(s"${valueToString(funval)} requires $n arguments but $m were given", funexp)
          }
        case _ => throw InterpreterError(s"${valueToString(funval)} is not a function expression", funexp)
      }
    case LambdaExp(params, body) =>
      ClosureVal(params, None, body, env, List.empty)
  }

  /**
    * Evaluates a declaration.
    */
  def eval(d: Decl, env: Env, b: BlockExp): Env = d match {
    case ValDecl(x, opttype, exp) =>
      env + (x -> eval(exp, env))
    case DefDecl(fun, params, optrestype, body) =>
      env + (fun -> ClosureVal(params, optrestype, body, env, b.defs))
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
        case (ClosureVal(cparams, optcrestype, _, _, _), FunType(paramtypes, restype)) if cparams.length == paramtypes.length =>
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
    case ClosureVal(params, _, exp, _, _) => // the resulting string ignores the result type annotation and the declaration environment
      s"<(${params.map(unparse).mkString(",")}), ${unparse(exp)}>"
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
