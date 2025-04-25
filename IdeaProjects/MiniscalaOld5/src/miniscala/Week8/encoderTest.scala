package miniscala.Week8
import miniscala.Interpreter.*
import miniscala.Lambda.{decodeBoolean, decodeNumber, encode}
import miniscala.parser.Parser.*

object encoderTest {
  def main(args: Array[String]): Unit = {

    def checkFun[T](s: String, f: Val => T): Boolean = {
      val result = eval(parse(s), makeInitialEnv(parse(s))) match {
        case IntVal(c) => c
        case BoolVal(c) => c
        case _ => assert(1 == 0)
      }
      val programEnc = encode(parse(s))
      val env = makeInitialEnv(programEnc)
      f(eval(programEnc, env)) == result
    }

    val numPrograms: List[String] = List("1+2",
      "{val x = 2; x}",
      "2-1",
      "{def f(n: Int): Int = if (n == 0) 1 else n * f(n-1); f(3)}",
      "if (!false) 1 else 2",
      //readFile("examples/tak2.s"),
      readFile("examples/mc91.s"))

    val boolPrograms: List[String] = List("0==0",
      "{val x = true; !x}",
      "1-1 == 0")
    for (p <- numPrograms) {
      assert(checkFun(p, decodeNumber))
    }
    for(p <- boolPrograms) {
      assert(checkFun(p, decodeBoolean))
    }
  }
}