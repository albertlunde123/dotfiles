{ val x = 1;
  { def q(a: Int): Int = x + a;
    { val x = 2;
      q(3)
    }
  }
}
