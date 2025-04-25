package miniscala

import miniscala.Ast.*
import miniscala.Unparser.unparse

/**
  * Type checker for MiniScala.
  */
object TypeChecker {

  type TypeEnv = Map[Id, Type]

  type ClassTypeEnv = Map[Id, StaticClassType]

  val unitType: Type = TupleType(Nil)

  def typeCheck(e: Exp, tenv: TypeEnv, ctenv: ClassTypeEnv): Type = e match {
    case IntLit(_) => IntType()
    case BoolLit(_) => BoolType()
    case FloatLit(_) => FloatType()
    case StringLit(_) => StringType()
    case NullLit() => NullType()
    case VarExp(x) => tenv.getOrElse(x, throw TypeError(s"Unknown identifier '$x'", e)) match {
      case MutableType(thetype) => thetype
      case t: Type => t
    }
    case BinOpExp(leftexp, op, rightexp) =>
      val lefttype = typeCheck(leftexp, tenv, ctenv)
      val righttype = typeCheck(rightexp, tenv, ctenv)
      op match {
        case PlusBinOp() =>
          (lefttype, righttype) match {
            case (IntType(), IntType()) => IntType()
            case (FloatType(), FloatType()) => FloatType()
            case (IntType(), FloatType()) => FloatType()
            case (FloatType(), IntType()) => FloatType()
            case (StringType(), StringType()) => StringType()
            case (StringType(), IntType()) => StringType()
            case (StringType(), FloatType()) => StringType()
            case (IntType(), StringType()) => StringType()
            case (FloatType(), StringType()) => StringType()
            case _ => throw TypeError(s"Type mismatch at '+', unexpected types ${unparse(lefttype)} and ${unparse(righttype)}", op)
          }
        case MinusBinOp() | MultBinOp() | DivBinOp() | ModuloBinOp() | MaxBinOp() =>
          (lefttype, righttype) match {
            case (IntType(), IntType()) => IntType()
            case (FloatType(), FloatType()) => FloatType()
            case (IntType(), FloatType()) => FloatType()
            case (FloatType(), IntType()) => FloatType()
            case _ => throw TypeError(s"Type mismatch at ${op} unexpected types ${lefttype} and ${righttype}", op)
          }
        case EqualBinOp() => BoolType()
        case LessThanBinOp() | LessThanOrEqualBinOp() =>
          (lefttype, righttype) match {
            case (IntType(), IntType()) => BoolType()
            case (FloatType(), FloatType()) => BoolType()
            case (IntType(), FloatType()) => BoolType()
            case (FloatType(), IntType()) => BoolType()
            case _ => throw TypeError(s"Type mismatch at ${op} unexpected types ${lefttype} and ${righttype}", op)
          }
        case AndBinOp() | OrBinOp() =>
          (lefttype, righttype) match {
            case (BoolType(), BoolType()) => BoolType()
            case _ => throw TypeError(s"Type mismatch at ${op} unexpected types ${lefttype} and ${righttype}", op)
          }
      }
    case UnOpExp(op, exp) => 
      val exptype = typeCheck(exp, tenv, ctenv)
      op match {
        case NegUnOp() =>
          exptype match {
            case IntType() => IntType()
            case FloatType() => FloatType()
            case _ => throw TypeError(s"Type mismatch at ${op} unexpected types ${exptype}", op)
          }
        case NotUnOp() =>
          exptype match {
            case BoolType() => BoolType()
            case _ => throw TypeError(s"Type mismatch at ${op} unexpected types ${exptype}", op)
          }
      }
    case IfThenElseExp(condexp, thenexp, elseexp) =>
      val condtype = typeCheck(condexp, tenv, ctenv)
      if (condtype != BoolType()) {
        throw TypeError("condition should be boolean", condexp)
      }
      val thentype = typeCheck(thenexp, tenv, ctenv)
      val elsetype = typeCheck(elseexp, tenv, ctenv)
      // skal maaske aendres.
      checkSubtype(thentype, elsetype, e)
      thentype
      
      //else throw TypeError("then and else statement should be of the same type", e)
    case BlockExp(vals, vars, defs, classes, exp) =>
      var tenv1 = tenv
      var ctenv1 = ctenv
      for (d <- vals) {
        val t = typeCheck(d.exp, tenv1, ctenv1)
        val ot = getType(d.opttype, ctenv1)
        checkSubtype(t, ot, d)
        tenv1 = tenv1 + (d.x -> ot.getOrElse(t))
      }
      for (d <- vars) {
        val t = typeCheck(d.exp, tenv1, ctenv1)
        val ot = getType(d.opttype, ctenv1)
        checkSubtype(t, ot,  d)
        tenv1 = tenv1 + (d.x -> MutableType(ot.getOrElse(t)))
      }

      // extend the type environment with the function types.
      for (d <- defs) { 
        val dtype = makeFunType(d, ctenv)
        tenv1 = tenv1 + (d.fun -> dtype)
      }
      // we create a temporary environment for type-checking the body
      for (d <- defs) {
        var tempTenv = tenv1
        val ftype = makeFunType(d, ctenv)
        for ((a, p) <- ftype.paramtypes.zip(d.params)) {
          tempTenv = tempTenv + (p.x -> a)
        }
        val bodyType = typeCheck(d.body, tempTenv, ctenv1)
        checkSubtype(bodyType, Some(ftype.restype), d)
      }
      // extend the class environment with the class-types
      for (c <- classes) {
        val ctype = makeStaticClassType(c, ctenv1, classes)
        ctenv1 = ctenv1 + (c.klass -> ctype)
      }

      for (c <- classes) {
        var bodyTenv = tenv1
        for (p <- c.params) {
          val ptype = getType(p.opttype.getOrElse(throw TypeError("missing annotation for class parameter", c)), ctenv1)
          bodyTenv = bodyTenv + (p.x -> ptype)
        }
        val c1 = typeCheck(c.body, bodyTenv, ctenv1)
      }
      var v1 = unitType

      for (e <- exp) {
        v1 = typeCheck(e, tenv1, ctenv1)
      }
      v1
    case TupleExp(exps) => TupleType(exps.map(exp => typeCheck(exp, tenv, ctenv)))
    case MatchExp(exp, cases) =>
      val exptype = typeCheck(exp, tenv, ctenv)
      exptype match {
        case TupleType(ts) =>
          var res: Option[Type] = None
          for (c <- cases) {
            if (ts.length == c.pattern.length) {
              var newTenv = tenv
              for ((t, pat) <- ts.zip(c.pattern)) {
                newTenv = newTenv + (pat -> t)
              }
              val caseType = typeCheck(c.exp, newTenv, ctenv)
              res match {
                case None => res = Some(caseType)
                case Some(t) =>
                  if (t != caseType) {
                    throw TypeError("case expressions should be of the same type...", e)
                  }
              }
            }
          }
          res match {
            case Some(t) => t
            case None => throw TypeError(s"No case matches type ${unparse(exptype)}", e)
          }
        case _ => throw TypeError(s"Tuple expected at match, found ${unparse(exptype)}", e)
      }
    case CallExp(funexp, args) =>
      // As with the interpreter, a funexp can be both a VarExp and a LambdaExp,
      // but they both give a FunType when type checked.
      val ftype = typeCheck(funexp, tenv, ctenv) match {
        case FunType(p, r) => FunType(p, r)
        case _ => throw TypeError("funexp should be FunType", e)
      }
      if (ftype.paramtypes.length != args.length) {
        throw TypeError(s"Incorrect number of arguments for function", e)
      }
      for ((a, p) <- args.zip(ftype.paramtypes)) {
        checkSubtype(typeCheck(a, tenv, ctenv), Some(p), a)
      }
      ftype.restype

    case LambdaExp(params, body) =>
      var tempTenv = tenv
      var pTypes = List[Type]()
      for (p <- params) {
        // we use getType when looking up the parameters.
        val ptyp = getType(p.opttype,  ctenv).getOrElse(throw TypeError("type annotation missing for parameter", p))
        tempTenv = tempTenv + (p.x -> ptyp)
        pTypes = pTypes :+ ptyp
      }
      val bodyType = typeCheck(body, tempTenv, ctenv)
      FunType(pTypes, bodyType)

    case AssignmentExp(x, exp) =>
      val xtype = tenv.getOrElse(x, throw TypeError(s"${x} is not declared.", e)) match {
        case MutableType(typ) => typ
        case _ => throw TypeError(s"${x} is not mutable", e)
      }
      checkSubtype(typeCheck(exp, tenv, ctenv), Some(xtype), e)
      unitType
    case WhileExp(cond, body) =>
      val condType = typeCheck(cond, tenv, ctenv) match {
        case BoolType() =>
        case _ => throw TypeError("condition in while loop should be boolean", e)
      }
      val bodyType = typeCheck(body, tenv, ctenv)
      unitType

    case NewObjExp(klass, args) =>
      val ctype = ctenv.getOrElse(klass, throw TypeError(s"${klass} class is not declared.", e)) match {
        case StaticClassType(srcpos, params, membertypes, ctenv, classes) =>
          val ctenv1 = rebindClasses(ctenv, classes)
          val ptypes = params.map(p => getType(p, ctenv1))
          if (params.length != args.length) {
            throw TypeError("Incorrect number of arguments in new object", e)
          }
          for ((a, p) <- args.zip(ptypes)) {
            val atype = typeCheck(a, tenv, ctenv1)
            checkSubtype(atype, p, e)
          }
          StaticClassType(srcpos, params, membertypes, ctenv1, classes)
        case _ => throw TypeError("class is not defined", e)
      }
      ctype

    case LookupExp(objexp, member) =>
      val mtype = typeCheck(objexp, tenv, ctenv) match {
        case StaticClassType(_, _, m, innerctenv, classes) =>
          val ctenv1 = rebindClasses(innerctenv, classes)
          getType(m.getOrElse(member, throw TypeError(s"unknown attribute ${member}", e)), ctenv1)
        case _ => throw TypeError("Unable to lookup non-class object", e)
      }
      mtype
  }

  /**
   * Checks whether `t1` is a subtype of `t2`.
   */
  def subtype(t1: Type, t2: Type): Boolean = (t1, t2) match {
    case (IntType(), FloatType()) => true
    case (NullType(), StaticClassType(_,_,_,_,_)) => true
    case (StaticClassType(p1,_,_,_,_), StaticClassType(p2,_,_,_,_)) => p1 == p2
    case (FunType(p1, r1), FunType(p2, r2)) => subtype(TupleType(p2), TupleType(p1)) && subtype(r1, r2)
    case (TupleType(t1), TupleType(t2)) =>
      if (t1.length != t2.length) false else {
        var a = true
        for ((v, w) <- t1.zip(t2)) {
          if (!subtype(v, w)) {
            a = false
          }
        }
        a
      }
    case _ =>
      println(t1)
      println(t2)
      t1 == t2
  }

  /**
   * Checks whether `t1` is a subtype of `t2`, generates type error otherwise.
   */
  def checkSubtype(t1: Type, t2: Type, n: AstNode): Unit =
    if (!subtype(t1, t2)) throw new TypeError(s"Type mismatch: type ${unparse(t1)} is not subtype of ${unparse(t2)}", n)

  /**
   * Checks whether `t1` is a subtype of `ot2` (if present), generates type error otherwise.
   */
  def checkSubtype(t: Type, ot2: Option[Type], n: AstNode): Unit = ot2 match {
    case Some(t2) => checkSubtype(t, t2, n)
    case None => // do nothing
  }
  /**
    * Returns the type described by the type annotation `t`.
    * Class names are converted to proper types according to the class type environment `ctenv`.
    */
  def getType(t: Type, ctenv: ClassTypeEnv): Type = t match {
    case ClassNameType(klass) => ctenv.getOrElse(klass, throw TypeError(s"Unknown class '$klass'", t))
    case IntType() | BoolType() | FloatType() | StringType() | NullType() => t
    case TupleType(ts) => TupleType(ts.map(tt => getType(tt, ctenv)))
    case FunType(paramtypes, restype) => FunType(paramtypes.map(tt => getType(tt, ctenv)), getType(restype, ctenv))
    case _ => throw RuntimeException(s"Unexpected type $t")
  }

  /**
    * Returns the type described by the optional type annotation `ot` (if present).
    */
  def getType(ot: Option[Type], ctenv: ClassTypeEnv): Option[Type] = ot.map(t => getType(t, ctenv))

  /**
    * Returns the function type for the function declaration `d`.
    */
  // I have made some changes here, makeFunType now takes a ClassTypeEnv
  // and uses getType to resolve the parameters and result
  def makeFunType(d: DefDecl, ctenv: ClassTypeEnv): FunType =
    FunType(d.params.map(p => getType(p.opttype.getOrElse(throw TypeError(s"Type annotation missing at parameter ${p.x}", p)), ctenv)),
      getType(d.optrestype.getOrElse(throw TypeError(s"Type annotation missing at function result ${d.fun}", d)), ctenv))

  /**
    * Returns the class type for the class declaration `d`.
    */
  // We might be able to remove the getType from the function part, as it has already been called by makeFunType.
  def makeStaticClassType(d: ClassDecl, ctenv: ClassTypeEnv, classes: List[ClassDecl]): StaticClassType = {
    var membertypes: TypeEnv = Map()
    for (m <- d.body.vals)
      membertypes = membertypes + (m.x -> m.opttype.getOrElse(throw TypeError(s"Type annotation missing at field ${m.x}", m)))
    for (m <- d.body.vars)
      membertypes = membertypes + (m.x -> m.opttype.getOrElse(throw TypeError(s"Type annotation missing at field ${m.x}", m)))
    for (m <- d.body.defs)
      membertypes = membertypes + (m.fun -> getType(makeFunType(m, ctenv), ctenv))
    StaticClassType(d.pos, d.params.map(f => f.opttype.getOrElse(throw TypeError(s"Type annotation missing at parameter ${f.x}", d))), membertypes, ctenv, classes)
  }

  def rebindClasses(ctenv: ClassTypeEnv, classes: List[ClassDecl]): ClassTypeEnv = {
    var ctenv1 = ctenv
    for (c <- classes) {
      val ctype = makeStaticClassType(c, ctenv1, classes)
      ctenv1 = ctenv1 + (c.klass -> ctype)
    }
    ctenv1
  }

  /**
    * Checks that the types `t1` and `ot2` are equal (if present), throws type error exception otherwise.
    */
  def checkTypesEqual(t1: Type, ot2: Option[Type], n: AstNode): Unit = ot2 match {
    case Some(t2) =>
      if (t1 != t2)
        throw TypeError(s"Type mismatch: expected type ${unparse(t2)}, found type ${unparse(t1)}", n)
    case None => // do nothing
  }

  /**
    * Builds an initial type environment, with a type for each free variable in the program.
    */
  def makeInitialTypeEnv(program: Exp): TypeEnv = {
    var tenv: TypeEnv = Map()
    for (x <- Vars.freeVars(program))
      tenv = tenv + (x -> IntType())
    tenv
  }

  /**
    * Exception thrown in case of MiniScala type errors.
    */
  class TypeError(msg: String, node: AstNode) extends MiniScalaError(s"Type error: $msg", node.pos)
}
