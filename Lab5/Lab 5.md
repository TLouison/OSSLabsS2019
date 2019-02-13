# Lab 5
### Todd Louison

## CMake Tutorial
### Part 1

```cmake
project(Tutorial)

add_executable(Tutorial tutorial.cxx)
```

### Part 2

```cmake
cmake_minimum_required(VERSION 3.3)
project(Tutorial)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# the version number.
set(Tutorial_VERSION_MAJOR 1)
set(Tutorial_VERSION_MINOR 0)

# configure a header file to pass some of the CMake settings
# to the source code
configure_file(
  "${PROJECT_SOURCE_DIR}/TutorialConfig.h.in"
  "${PROJECT_BINARY_DIR}/TutorialConfig.h"
  )

# add the executable
add_executable(Tutorial tutorial.cxx)

# add the binary tree to the search path for include files
# so that we will find TutorialConfig.h
target_include_directories(Tutorial PUBLIC
                           "${PROJECT_BINARY_DIR}"
                           )

```

### Part 3

```cmake
cmake_minimum_required(VERSION 3.3)
project(Tutorial)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# should we use our own math functions
option(USE_MYMATH "Use tutorial provided math implementation" ON)

# the version number.
set(Tutorial_VERSION_MAJOR 1)
set(Tutorial_VERSION_MINOR 0)

# configure a header file to pass some of the CMake settings
# to the source code
configure_file(
  "${PROJECT_SOURCE_DIR}/TutorialConfig.h.in"
  "${PROJECT_BINARY_DIR}/TutorialConfig.h"
  )

# add the MathFunctions library?
if(USE_MYMATH)
  add_subdirectory(MathFunctions)
  list(APPEND EXTRA_LIBS MathFunctions)
  list(APPEND EXTRA_INCLUDES "${PROJECT_SOURCE_DIR}/MathFunctions")
endif(USE_MYMATH)

# add the executable
add_executable(Tutorial tutorial.cxx)

target_link_libraries(Tutorial ${EXTRA_LIBS})

# add the binary tree to the search path for include files
# so that we will find TutorialConfig.h
target_include_directories(Tutorial PUBLIC
                           "${PROJECT_BINARY_DIR}"
                           ${EXTRA_INCLUDES}
                           )

```

### Step 4

```cmake
cmake_minimum_required(VERSION 3.3)
project(Tutorial)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# should we use our own math functions
option(USE_MYMATH "Use tutorial provided math implementation" ON)

# the version number.
set(Tutorial_VERSION_MAJOR 1)
set(Tutorial_VERSION_MINOR 0)

# configure a header file to pass some of the CMake settings
# to the source code
configure_file(
  "${PROJECT_SOURCE_DIR}/TutorialConfig.h.in"
  "${PROJECT_BINARY_DIR}/TutorialConfig.h"
  )

# add the MathFunctions library?
if(USE_MYMATH)
  add_subdirectory(MathFunctions)
  list(APPEND EXTRA_LIBS MathFunctions)
endif(USE_MYMATH)

# add the executable
add_executable(Tutorial tutorial.cxx)

target_link_libraries(Tutorial PUBLIC ${EXTRA_LIBS})

# add the binary tree to the search path for include files
# so that we will find TutorialConfig.h
target_include_directories(Tutorial PUBLIC
                           "${PROJECT_BINARY_DIR}"
                           )

```

### Step 5

```cmake
cmake_minimum_required(VERSION 3.3)
project(Tutorial)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# should we use our own math functions
option(USE_MYMATH "Use tutorial provided math implementation" ON)

# the version number.
set(Tutorial_VERSION_MAJOR 1)
set(Tutorial_VERSION_MINOR 0)

# configure a header file to pass some of the CMake settings
# to the source code
configure_file(
  "${PROJECT_SOURCE_DIR}/TutorialConfig.h.in"
  "${PROJECT_BINARY_DIR}/TutorialConfig.h"
  )

# add the MathFunctions library?
if(USE_MYMATH)
  add_subdirectory(MathFunctions)
  list(APPEND EXTRA_LIBS MathFunctions)
endif()

# add the executable
add_executable(Tutorial tutorial.cxx)
target_link_libraries(Tutorial PUBLIC ${EXTRA_LIBS})

# add the binary tree to the search path for include files
# so that we will find TutorialConfig.h
target_include_directories(Tutorial PUBLIC
                           "${PROJECT_BINARY_DIR}"
                           )

# add the install targets
install(TARGETS Tutorial DESTINATION bin)
install(FILES "${PROJECT_BINARY_DIR}/TutorialConfig.h"
  DESTINATION include
  )

# enable testing
enable_testing()

# does the application run
add_test(NAME Runs COMMAND Tutorial 25)

# does the usage message work?
add_test(NAME Usage COMMAND Tutorial)
set_tests_properties(Usage
  PROPERTIES PASS_REGULAR_EXPRESSION "Usage:.*number"
  )

# define a function to simplify adding tests
function(do_test target arg result)
  add_test(NAME Comp${arg} COMMAND ${target} ${arg})
  set_tests_properties(Comp${arg}
    PROPERTIES PASS_REGULAR_EXPRESSION ${result}
    )
endfunction(do_test)

# do a bunch of result based tests
do_test(Tutorial 4 "4 is 2")
do_test(Tutorial 9 "9 is 3")
do_test(Tutorial 5 "5 is 2.236")
do_test(Tutorial 7 "7 is 2.645")
do_test(Tutorial 25 "25 is 5")
do_test(Tutorial -25 "-25 is [-nan|nan|0]")
do_test(Tutorial 0.0001 "0.0001 is 0.01")

```



## Creating Makefiles and CMake files

### Makefile

```makefile
all: dynamic static
dynamic: dynamic.o libblock.so
	gcc dynamic.o libblock.so -o dynamic -Wl,-rpath='$$ORIGIN'
static: static.o libblock.so
	gcc static.o libblock.so -o dynamic -Wl,-rpath='$$ORIGIN'
dynamic.o: dynamic_block.c
	gcc dynamic_block.c -o dynamic.o
static.o: static_block.c
	gcc static_block.c -o static.o
libblock.so: block.o
	gcc -shared -o libblock.so block.o
block.o: source/block.c headers/block.h
	gcc -fPIC -c source/block.c -o block.o

```

### CMake File

```cmake
cmake_minimum_required(VERSION 3.0)
project(CMakeTest C)

add_library(block SHARED source/block.c headers/block.h)

add_executable(dynamic dynamic_block.c)
target_link_libraries(dynamic block)

add_executable(static static_block.c)
target_link_libraries(static block)
```

### CMake Makefile

```makefile
# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.13

# Default target executed when no arguments are given to make.
default_target: all

.PHONY : default_target

# Allow only one "make -f Makefile2" at a time, but pass parallelism.
.NOTPARALLEL:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/local/Cellar/cmake/3.13.4/bin/cmake

# The command to remove a file.
RM = /usr/local/Cellar/cmake/3.13.4/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /Users/todd/Documents/School/Junior/S2/OSS/Labs/Lab5/lab-example

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /Users/todd/Documents/School/Junior/S2/OSS/Labs/Lab5/lab-example

#=============================================================================
# Targets provided globally by CMake.

# Special rule for the target rebuild_cache
rebuild_cache:
        @$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --cyan "Running CMake to regenerate build system..."
        /usr/local/Cellar/cmake/3.13.4/bin/cmake -S$(CMAKE_SOURCE_DIR) -B$(CMAKE_BINARY_DIR)
.PHONY : rebuild_cache

# Special rule for the target rebuild_cache
rebuild_cache/fast: rebuild_cache

.PHONY : rebuild_cache/fast

# Special rule for the target edit_cache
edit_cache:
        @$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --cyan "Running CMake cache editor..."
        /usr/local/Cellar/cmake/3.13.4/bin/ccmake -S$(CMAKE_SOURCE_DIR) -B$(CMAKE_BINARY_DIR)
.PHONY : edit_cache

# Special rule for the target edit_cache
edit_cache/fast: edit_cache

.PHONY : edit_cache/fast

# The main all target
all: cmake_check_build_system
        $(CMAKE_COMMAND) -E cmake_progress_start /Users/todd/Documents/School/Junior/S2/OSS/Labs/Lab5/lab-example/CMakeFiles /Users/todd/Documents/School/Junior/S2/OSS/Labs/Lab5/lab-example/CMakeFiles/progress.marks
        $(MAKE) -f CMakeFiles/Makefile2 all
        $(CMAKE_COMMAND) -E cmake_progress_start /Users/todd/Documents/School/Junior/S2/OSS/Labs/Lab5/lab-example/CMakeFiles 0
.PHONY : all

# The main clean target
clean:
        $(MAKE) -f CMakeFiles/Makefile2 clean
.PHONY : clean

# The main clean target
clean/fast: clean

.PHONY : clean/fast

# Prepare targets for installation.
preinstall: all
        $(MAKE) -f CMakeFiles/Makefile2 preinstall
.PHONY : preinstall

# Prepare targets for installation.
preinstall/fast:
        $(MAKE) -f CMakeFiles/Makefile2 preinstall
.PHONY : preinstall/fast

# clear depends
depend:
        $(CMAKE_COMMAND) -S$(CMAKE_SOURCE_DIR) -B$(CMAKE_BINARY_DIR) --check-build-system CMakeFiles/Makefile.cmake 1
.PHONY : depend

#=============================================================================
# Target rules for targets named static

# Build rule for target.
static: cmake_check_build_system
        $(MAKE) -f CMakeFiles/Makefile2 static
.PHONY : static

# fast build rule for target.
static/fast:
        $(MAKE) -f CMakeFiles/static.dir/build.make CMakeFiles/static.dir/build
.PHONY : static/fast

#=============================================================================
# Target rules for targets named dynamic

# Build rule for target.
dynamic: cmake_check_build_system
        $(MAKE) -f CMakeFiles/Makefile2 dynamic
.PHONY : dynamic

# fast build rule for target.
dynamic/fast:
        $(MAKE) -f CMakeFiles/dynamic.dir/build.make CMakeFiles/dynamic.dir/build
.PHONY : dynamic/fast

#=============================================================================
# Target rules for targets named block

# Build rule for target.
block: cmake_check_build_system
        $(MAKE) -f CMakeFiles/Makefile2 block
.PHONY : block

# fast build rule for target.
block/fast:
        $(MAKE) -f CMakeFiles/block.dir/build.make CMakeFiles/block.dir/build
.PHONY : block/fast

dynamic_block.o: dynamic_block.c.o

.PHONY : dynamic_block.o

# target to build an object file
dynamic_block.c.o:
        $(MAKE) -f CMakeFiles/dynamic.dir/build.make CMakeFiles/dynamic.dir/dynamic_block.c.o
.PHONY : dynamic_block.c.o

dynamic_block.i: dynamic_block.c.i

.PHONY : dynamic_block.i

# target to preprocess a source file
dynamic_block.c.i:
        $(MAKE) -f CMakeFiles/dynamic.dir/build.make CMakeFiles/dynamic.dir/dynamic_block.c.i
.PHONY : dynamic_block.c.i

dynamic_block.s: dynamic_block.c.s

.PHONY : dynamic_block.s

# target to generate assembly for a file
dynamic_block.c.s:
        $(MAKE) -f CMakeFiles/dynamic.dir/build.make CMakeFiles/dynamic.dir/dynamic_block.c.s
.PHONY : dynamic_block.c.s

source/block.o: source/block.c.o

.PHONY : source/block.o

# target to build an object file
source/block.c.o:
        $(MAKE) -f CMakeFiles/block.dir/build.make CMakeFiles/block.dir/source/block.c.o
.PHONY : source/block.c.o

source/block.i: source/block.c.i

.PHONY : source/block.i

# target to preprocess a source file
source/block.c.i:
        $(MAKE) -f CMakeFiles/block.dir/build.make CMakeFiles/block.dir/source/block.c.i
.PHONY : source/block.c.i

source/block.s: source/block.c.s

.PHONY : source/block.s

# target to generate assembly for a file
source/block.c.s:
        $(MAKE) -f CMakeFiles/block.dir/build.make CMakeFiles/block.dir/source/block.c.s
.PHONY : source/block.c.s

static_block.o: static_block.c.o

.PHONY : static_block.o

# target to build an object file
static_block.c.o:
        $(MAKE) -f CMakeFiles/static.dir/build.make CMakeFiles/static.dir/static_block.c.o
.PHONY : static_block.c.o

static_block.i: static_block.c.i

.PHONY : static_block.i

# target to preprocess a source file
static_block.c.i:
        $(MAKE) -f CMakeFiles/static.dir/build.make CMakeFiles/static.dir/static_block.c.i
.PHONY : static_block.c.i

static_block.s: static_block.c.s

.PHONY : static_block.s

# target to generate assembly for a file
static_block.c.s:
        $(MAKE) -f CMakeFiles/static.dir/build.make CMakeFiles/static.dir/static_block.c.s
.PHONY : static_block.c.s

# Help Target
help:
        @echo "The following are some of the valid targets for this Makefile:"
        @echo "... all (the default if no target is provided)"
        @echo "... clean"
        @echo "... depend"
        @echo "... rebuild_cache"
        @echo "... edit_cache"
        @echo "... static"
        @echo "... dynamic"
        @echo "... block"
        @echo "... dynamic_block.o"
        @echo "... dynamic_block.i"
        @echo "... dynamic_block.s"
        @echo "... source/block.o"
        @echo "... source/block.i"
        @echo "... source/block.s"
        @echo "... static_block.o"
        @echo "... static_block.i"
        @echo "... static_block.s"
.PHONY : help



#=============================================================================
# Special targets to cleanup operation of make.

# Special rule to run CMake to check the build system integrity.
# No rule that depends on this can have commands that come from listfiles
# because they might be regenerated.
cmake_check_build_system:
        $(CMAKE_COMMAND) -S$(CMAKE_SOURCE_DIR) -B$(CMAKE_BINARY_DIR) --check-build-system CMakeFiles/Makefile.cmake 0
.PHONY : cmake_check_build_system
```



## Size Difference

My program complied with the static library was much bigger than the shared library program.

