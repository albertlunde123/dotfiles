package miniscala.Week3
import miniscala.parser.Parser.parse
import miniscala.Unparser.unparse


object UnparserTest {
  def main(args: Array[String]): Unit = {
    val a = parse("{val a: Int = 2; def foo(x: Int): Int = x + 2; foo(4) + a}")
    
    val b = parse("c match {case (a, b) => a + b \n" +
      "case (a, b) => a + b}")
    
    println(b)
    
    println(unparse(b))
    println(unparse(a))
  }
}