ThisBuild / scalaVersion := "3.6.2" // Replace with your Scala version

lazy val root = (project in file("."))
  .settings(
    name := "Miniscala", // Replace with your project name
    version := "0.1.0",
    libraryDependencies ++= Seq(
      // Add your dependencies here
      "org.scala-lang.modules" %% "scala-parser-combinators" % "2.1.0"
    )
  )

