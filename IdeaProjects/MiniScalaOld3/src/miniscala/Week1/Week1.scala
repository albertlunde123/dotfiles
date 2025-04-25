package miniscala.Week1

import miniscala.Ast.*
import miniscala.parser.Parser

object Week1 {
  def main(args: Array[String]): Unit = {
    val a1 = BinOpExp(IntLit(2), MinusBinOp(), IntLit(10))
    val a2 = Parser.parse("2-10")
    println(a2)
    println("a1 and a2 are equal: " + (a2 == a1))
  }
}
