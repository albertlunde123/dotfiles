package miniscala.Week13

import miniscala.AbstractMachine._
import miniscala.Compiler._
import miniscala.parser.Parser.parse

object Test132 {

  def main(args: Array[String]): Unit = {
    test("2 + 3", 5)
    test("4 * 3", 12)
    test("if (2 == 2) 1 else 0", 1)
    test("if (2 == 1) 1 else 0", 0)
    test("if (2 <= 2) 1 else 0", 1)
    test("if (2 <= 1) 1 else 0", 0)
    test("if (2 < 2) 1 else 0", 0)
    test("if (2 < 3) 1 else 0", 1)
    test("if (2 == 2 & 1 == 1) 1 else 0", 1)
    test("if (2 == 2 | 1 == 0) 1 else 0", 1)
    test("1 + {val x = 1; x}", 2)
    test("1 + {val x = 1; val y = 1; x+y}", 3)
    test("if (2 == 2) 1 else 0", 1)
    // <-- add more test cases here

    println("All tests passed successfully!")
  }

  def test(prg: String, result: Int): Unit = {
    assert(execute(compile(parse(prg)), Nil) == result)
  }
}