package miniscala

import miniscala.Ast.*
import miniscala.Unparser.unparse

import scala.io.StdIn
import scala.util.parsing.input.Position

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
                   var env: Env,
                   val cenv: ClassEnv) extends Val

  object ClosureVal {
    def apply(params: List[FunParam], optrestype: Option[Type], body: Exp, env: Env, cenv: ClassEnv) =
      new ClosureVal(params, optrestype, body, env, cenv)

    def unapply(cl: ClosureVal): Option[(List[FunParam], Option[Type], Exp, Env, ClassEnv)] =
      Some((cl.params, cl.optrestype, cl.body, cl.env, cl.cenv))
  }

  case class RefVal(loc: Loc, opttype: Option[Type]) extends Val
  case class ObjRefVal(loc: Loc, opttype: Option[Type]) extends Val
  case class ObjectVal(members: Env) extends Val
  case class Constructor(params: List[FunParam], body: BlockExp, env: Env, cenv: ClassEnv, classes: List[ClassDecl], srcpos: Position)

  val unitVal: Val = TupleVal(Nil)
  type Env = Map[Id, Val]
  type ClassEnv = Map[Id, Constructor]

  val sto = new scala.collection.mutable.ArrayBuffer[Val]
  type Loc = Int


  /**
    * Evaluates an expression.
    */
  def eval(e: Exp, env: Env, cenv: ClassEnv): Val = e match {
    case IntLit(c) => IntVal(c)
    case BoolLit(c) => BoolVal(c)
    case FloatLit(c) => FloatVal(c)
    case StringLit(c) => StringVal(c)
    case NullLit() => ???
    case VarExp(x) =>
      getValue(env.getOrElse(x, throw InterpreterError(s"Unknown identifier '$x'", e)))
    case BinOpExp(leftexp, op, rightexp) =>
      val leftval = eval(leftexp, env, cenv)
      val rightval = eval(rightexp, env, cenv)
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
      val expval = eval(exp, env, cenv)
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
      val condval = eval(condexp, env, cenv)
      condval match {
        case BoolVal(v) => if (v) eval(thenexp, env, cenv) else eval(elseexp, env, cenv)
        case _ => throw InterpreterError(s"Type mismatch at 'IfThenElse', unexpected value ${valueToString(condval)}", condexp)
    }
    case b: BlockExp =>
      val (res, _) = evalBlock(b, env, cenv)
      res

    case TupleExp(exps) =>
      var vals = List[Val]()
      for (exp <- exps) {
        val v = eval(exp, env, cenv)
        vals = v :: vals
      }
      TupleVal(vals.reverse)

    case MatchExp(exp, cases) =>
      val expval = eval(exp, env, cenv)
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
              res = Some(eval(c.exp, newEnv, cenv))
            }
          }
          res match {
            case Some(v) => v
            case None => throw InterpreterError(s"No case matches value ${valueToString(expval)}", e)
          }
        case _ => throw InterpreterError(s"Tuple expected at match, found ${valueToString(expval)}", e)
      }

    // used when declaring a new object
    case NewObjExp(klass, args) =>
      // check whether the class exists, and then retrieve it if it does
      val c = cenv.getOrElse(klass, throw InterpreterError(s"Unknown class name '$klass'", e))
      // extend the environment with any classes defined within, allowing for recursion.
      val declcenv1 = rebindClasses(c.env, c.cenv, c.classes)
      // evaluate any arguments given when creating the instance, and retrieve the resulting environment
      val declenv1 = evalArgs(args, c.params, env, cenv, c.env, declcenv1, e)
      // evaluate the class' body {a block}, and retrieve the resulting environment
      val (_, env1) = evalBlock(c.body, declenv1, declcenv1)
      // allocate a new location in the store.
      val newloc = sto.length
      // create a map containing pointers for everything defined in the class. functions, vals and vars.
      val objenv = (c.body.defs.map(d => d.fun -> env1(d.fun)) ++
        c.body.vars.map(d => d.x -> env1(d.x)) ++
        c.body.vals.map(d => d.x -> env1(d.x))).toMap
      // add the object to the store
      sto += ObjectVal(objenv)
      // create the pointer to the store, which will be added to environment.
      ObjRefVal(newloc, Some(DynamicClassType(c.srcpos)))

    // used when accessing fields or methods of a class.
    case LookupExp(objexp, member) =>
      val objval = eval(objexp, env, cenv)
      // return the object
      objval match {
        case ObjRefVal(loc, _) =>
          sto(loc) match {
            // return the specific field we are looking for
            case ObjectVal(members) =>
              getValue(members.getOrElse(member, throw InterpreterError(s"No such member: $member", e)))
            case _ => throw RuntimeException(s"Expected an object value")
          }
        case _ => throw InterpreterError(s"Base value of lookup is not a reference to an object: ${valueToString(objval)}", e)
      }

    case CallExp(funexp, args) =>
      // We can expect funexp to be a variable VarExp or a LambdaExp
      // Evaluating either of these will give a ClosureVal, in the lambda case optrestype = None and
      // defs is an empty list. But as they are still ClosureVal, we can just evaluate them.
      val funVal = eval(funexp, env, cenv)
      val closure = funVal match {
        case ClosureVal(params, optrestype, body, env, cenv) =>
          ClosureVal(params, optrestype, body, env, cenv)
        case _ => throw InterpreterError(s"Unknown function ${funexp}", e)
      }
      // create the environment where we evaluate the function
      val newEnv = evalArgs(args, closure.params, env, cenv, closure.env, cenv, e)
      // evaluate the function body in the correct environment
      val ret = eval(closure.body, newEnv, cenv)
      // dynamic type-checking
      // checkValueType(ret, getType(Some(ret), cenv), e)
      checkValueType(ret, getType(closure.optrestype, cenv), e)
      ret

    case LambdaExp(params, body) =>
      ClosureVal(params, None, body, env, cenv)

    case AssignmentExp(x, exp) =>
      val v1 = eval(exp, env, cenv)
      val (loc, t1) = env.getOrElse(x, throw InterpreterError(s"variable ${x} not declared", e)) match {
        case RefVal(loc,  t1) =>
          checkValueType(v1, t1, e)
          (loc, t1)
        case _ => throw InterpreterError("variable doesn't have a location", e)
      }
      sto.update(loc, v1)
      unitVal

    case WhileExp(cond, body) =>
      val bool = eval(cond, env, cenv)
      bool match {
        case BoolVal(false) => unitVal
        case BoolVal(true) =>
          eval(body, env, cenv)
          eval(WhileExp(cond, body), env, cenv)
        case _ => throw InterpreterError("While-loop condition is not boolean", e)
      }
  }

  /**
   * Evaluates a declaration.
   */
  def eval(d: Decl, env: Env, cenv: ClassEnv, b: BlockExp): (Env, ClassEnv) = d match {
    case ValDecl(x, opttype, exp) =>
      val v = eval(exp, env, cenv)
      val ot = getType(opttype, cenv)
      checkValueType(v, ot, d)
      val env1 = env + (x -> v)
      (env1, cenv)

    case VarDecl(x, opttype, exp) =>
      val v = eval(exp, env, cenv)
      val ot = getType(opttype, cenv)
      checkValueType(v, ot, d)
      val l = sto.length
      val env1 = env + (x -> RefVal(l, opttype))
      sto += v
      (env1, cenv)

    case DefDecl(fun, params, optrestype, body) =>
      val closure = ClosureVal(params, optrestype, body, env, cenv)
      (env + (fun -> closure), cenv)

    case ClassDecl(klass, params, body) =>
      val cenv1 = cenv + (klass -> Constructor(params, body, env, cenv, b.classes, d.pos))
      (env, cenv1)
  }
  def evalBlock(b: BlockExp, env: Env, cenv: ClassEnv): (Val, Env) = {
    var env1 = env
    var cenv1 = cenv
    // loop through all types of declarations and evaluate them, each type of declaration is handled by its own case.
    // notice that Decl evaluations return both values and environments.
    for (d <- b.vals ++ b.vars ++ b.defs ++ b.classes) {
      val (env2, cenv2) = eval(d, env1, cenv1, b)
      env1 = env2
      cenv1 = cenv2
    }

    // extend the closures with all the definitions, allowing for recursion
    for (d <- b.defs) {
      env1(d.fun) match {
        case c: ClosureVal => c.env = env1
      }
    }

    var v1 = unitVal
    // evaluate all the expressions, return the last one.
    for (e <- b.exps) {
      val v2 = eval(e, env1, cenv1)
      v1 = v2
    }
    (v1, env1)
  }
  def evalArgs(args: List[Exp], params: List[FunParam], env: Env, cenv: ClassEnv, declenv: Env, declcenv: ClassEnv, e: Exp): Env = {
    // correct number of arguments
    if (args.length != params.length) throw InterpreterError("Wrong number of arguments at call/new", e)
    // extend the environment
    var env1 = declenv
    for ((p, arg) <- params.zip(args)) {
      // bind/evaluate the parameters and dynamic type-checking
      val argval = eval(arg, env, cenv)
      checkValueType(argval, getType(p.opttype, declcenv), arg)
      env1 = env1 + (p.x -> argval)
    }
    env1
  }

  /**
   * Resolves reference values by looking up the referenced value in the store.
   */
  def getValue(v: Val): Val = v match {
    // used in VarExp, if v is a reference we look it up in the store, else we return it.
    case RefVal(loc, _) => sto(loc)
    case _ => v
  }

  /**
   * Rebinds `classes` in `cenv` to support recursive class declarations.
   */
  def rebindClasses(env: Env, cenv: ClassEnv, classes: List[ClassDecl]): ClassEnv = {
    var cenv1 = cenv
    // rebind any class definitions in the current scope to all classes.
    for (d <- classes)
      cenv1 = cenv1 + (d.klass -> Constructor(d.params, d.body, env, cenv, classes, d.pos))
    cenv1
  }

  /**
   * Returns the type described by the type annotation `ot` (if present).
   * Class names are converted to proper types according to the class environment `cenv`.
   */
  def getType(ot: Option[Type], cenv: ClassEnv): Option[Type] = ot.map(t => {
    def getType(t: Type): Type = t match {
      case ClassNameType(klass) => DynamicClassType(cenv.getOrElse(klass, throw InterpreterError(s"Unknown class '$klass'", t)).srcpos)
      case IntType() | BoolType() | FloatType() | StringType() | NullType() => t
      case TupleType(ts) => TupleType(ts.map(getType))
      case FunType(paramtypes, restype) => FunType(paramtypes.map(getType), getType(restype))
      case _ => throw RuntimeException(s"Unexpected type $t")
    }
    getType(t)
  })

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
        case (ClosureVal(cparams, optcrestype, _, _, cenv), FunType(paramtypes, restype)) if cparams.length == paramtypes.length =>
          for ((p, t) <- cparams.zip(paramtypes))
            checkTypesEqual(t, getType(p.opttype, cenv), n)
          checkTypesEqual(restype, getType(optcrestype, cenv), n)
        case (ObjRefVal(_, Some(vd: DynamicClassType)), td: DynamicClassType) =>
          if (vd != td)
            throw InterpreterError(s"Type mismatch: object of type ${unparse(vd)} does not match type ${unparse(td)}", n)
        case (_, ClassNameType(_)) =>
          throw RuntimeException(s"Unexpected type $t (missing call to 'getType'?)")
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
    case RefVal(loc, _) => s"#$loc" // the resulting string ignores the type annotation
    case _ => throw RuntimeException(s"Unexpected value $v") // (unreachable case)
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
