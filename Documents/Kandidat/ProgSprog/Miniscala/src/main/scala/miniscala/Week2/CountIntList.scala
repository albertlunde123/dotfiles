package miniscala.Week2
import miniscala.parser.Parser.parse
import miniscala.Ast._

def countIntLists(exp: Exp): Int = exp match {
    case IntLit(_) => 1
    case BinOpExp(leftexp, _, rightexp) =>
      countIntLists(leftexp) + countIntLists(rightexp)
  }

object Test {
  def main(args: Array[String]): Unit = {
    val a = "2+2+5*10"
    val b = parse(a)
    val c = countIntLists(b)
    println(b)
    println(c)
  }
}