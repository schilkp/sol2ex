# sol2ex

Convert code solutions to exercises.

Usage:

```bash
> python3 sol2ex.py [Source solution file] [Destination excercise file]
```

Generates `exercise_file.c` from `solution_file.c` by removing all
solutions and uncommenting the exercises. Solutions and exercises
are delimited as follows:

```c
normal_code();

//$ START EX
// // TODO:  Find the correct function and call it.
// _______();
//$ END

//$ START SOL
correct_function();
//$ END

//$ START SOL
printf("Hi!\r\n");
//$ START EX
// printf("?");
//$ END

// if (0) { //$ EX
if(a == 0) { //$ SOL
}
```

Sol2ex would convert the above snippet to the following:

```c
normal_code();

// TODO:  Find the correct function and call it.
_______();


printf("?");

if (0) {
}
```

Provided test file:
```
> python3 sol2ex.py test_sol.c test_ex.c
```
