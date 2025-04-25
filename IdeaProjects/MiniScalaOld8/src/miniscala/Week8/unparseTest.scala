package miniscala.Week8

import miniscala.parser.Parser.*
import miniscala.Unparser.unparse


object unparseTset {
  def main(args: Array[String]): Unit = {
    val a = unparse(parse("{def f(x: Int) = x; f(2)}"))
    val b = readFile("examples/lambda1.s")
    println(b)
    println(parse(b))
    println(unparse(parse(b)))
  }
}