package miniscala.Week2
import miniscala.Ast.*
import miniscala.parser.Parser.parse
import miniscala.Unparser.unparse

def simplify(exp: Exp): Exp = exp match {
  case BlockExp(c, v, defs, e) =>
    var cs: List[ValDecl] = List()
    val es = e.map(simplify)
    for (vals <- c) {
      cs = cs :+ ValDecl(vals.x, vals.opttype, simplify(vals.exp))
    }
    BlockExp(cs, v, defs, es)
  case UnOpExp(NegUnOp(), UnOpExp(NegUnOp(), e)) => simplify(e)
  case UnOpExp(NegUnOp(), IntLit(0)) => IntLit(0)
  case BinOpExp(left, op, right) =>
    val simpLeft = simplify(left)
    val simpRight = simplify(right)
    def simplifyBinOp(exp: Exp): Exp = exp match {
      case BinOpExp(c, MultBinOp(), IntLit(1)) => c
      case BinOpExp(IntLit(1), MultBinOp(), c) => c
      case BinOpExp(c, MultBinOp(), IntLit(0)) => IntLit(0)
      case BinOpExp(IntLit(0), MultBinOp(), c) => IntLit(0)
      case BinOpExp(c, DivBinOp(), IntLit(1)) => c
      case BinOpExp(c, PlusBinOp(), IntLit(0)) => c
      case BinOpExp(IntLit(0), PlusBinOp(), c) => c
      case BinOpExp(c, MinusBinOp(), IntLit(0)) => c
      case BinOpExp(c1, MinusBinOp(), c2) if c1 == c2 => IntLit(0)
      case BinOpExp(c1, DivBinOp(), c2) if c1 == c2 => IntLit(1)
      case _ => exp
    }
    simplifyBinOp(BinOpExp(simpLeft, op, simpRight))
  case _ => exp
}

object SimplifyTest {
  def main(args: Array[String]): Unit = {
    val d = parse("{val x = -(-(2*1)); val y = -(-(-(3))); x * y * 1}")
    val d_simplified = "{val x = 2; val y = -3; x * y}"
    val a = parse("2*1*1+0/1-2")
    val a_simplified = "0"
    assert(unparse(simplify(d)) == d_simplified)
    assert(unparse(simplify(a)) == a_simplified)
  }
}
