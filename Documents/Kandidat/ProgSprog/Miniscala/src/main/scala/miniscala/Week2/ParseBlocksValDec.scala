package miniscala.Week2
import miniscala.parser.Parser.parse
import miniscala.Unparser.unparse

object ParseBlocksValDec {
  def main(args: Array[String]): Unit = {
    val a = parse("x + {val z = y / x; z * 2} + 12")
    val b = unparse(parse("2 * z"))
    // val c = unparse(parse("val x = y"))
    val d = parse("{val x = 2; val y = 3; x * y}")
    println(a)
    println(b)
    // println(c)
    println(d)
    println(unparse(d))
    println(unparse(a))
  }
}