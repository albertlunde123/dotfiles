package miniscala.Week1

import miniscala.Ast.*
import miniscala.parser.Parser

object Week1 {
  def main(args: Array[String]): Unit = {
    val a1 = List(2, 3)
    val a2 = List(1, 2, 3)
    println(a1.zip(a2))
  }
}
