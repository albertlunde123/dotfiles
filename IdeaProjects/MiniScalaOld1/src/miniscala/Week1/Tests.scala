package miniscala.Week1

import miniscala.Interpreter.eval
import miniscala.Unparser.unparse
import miniscala.parser.Parser.parse

object Tests {
  def main(args: Array[String]): Unit = {
    // Tests for the max function
    val b = "2max5"
    assert(eval(parse(b)) == 5)
    println("max function test completed")

    // Tests for the unparser
    val a = "2+2-5*4max10/5"
    println(parse(a))
    println(unparse(parse(a)))
    assert(unparse(parse(a)) == a)
    println("parse function test completed")

    println("all tests succeeded")
  }
}
