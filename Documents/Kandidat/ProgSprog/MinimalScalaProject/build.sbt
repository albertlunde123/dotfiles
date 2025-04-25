ThisBuild / scalaVersion := "3.6.2"

lazy val root = (project in file("."))
  .settings(
    name := "MinimalScalaProject",
    version := "0.1.0",
    // If you need any libraries, add them here.
    libraryDependencies ++= Seq(
      // Example: "org.scala-lang.modules" %% "scala-parser-combinators" % "2.1.0"
    )
  )
