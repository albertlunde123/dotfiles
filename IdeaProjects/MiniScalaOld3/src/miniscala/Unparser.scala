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
  def unparse(n: AstNode): String = ???

  /**
    * Unparse function for optional type annotations.
    */
  def unparse(ot: Option[Type]): String = ot match {
    case Some(t) => ": " + unparse(t)
    case None => ""
  }
}
