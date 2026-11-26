# Обёртка: собирает плагин Bongobs Cat отдельно от дерева OBS.
cmake_minimum_required(VERSION 3.15)
project(bongobs_cat_wrapper LANGUAGES C CXX)

set(PLUGIN_SRC "" CACHE PATH "Папка исходников плагина (после патчей)")
set(OBS_INCLUDE "" CACHE PATH "Папка libobs из исходников OBS (заголовки)")
set(OBS_LIB "" CACHE FILEPATH "obs.lib")

# Репозиторий плагина проверяет именно эту строку (см. его CMakeLists.txt)
set(CMAKE_EXE_LINKER_FLAGS "/machine:x64 /OPT:REF")
# Библиотека Cubism Core с динамической CRT (/MD) - как по умолчанию в CMake
set(CORE_CRL_MD ON)
# Не собирать лишнее у GLFW
set(GLFW_BUILD_EXAMPLES OFF CACHE BOOL "" FORCE)
set(GLFW_BUILD_TESTS OFF CACHE BOOL "" FORCE)
set(GLFW_BUILD_DOCS OFF CACHE BOOL "" FORCE)
set(GLFW_INSTALL OFF CACHE BOOL "" FORCE)

# В дереве OBS эту функцию даёт сам OBS. Здесь установка не нужна.
function(install_obs_plugin_with_data)
endfunction()

# Цель libobs, на которую ссылается CMakeLists плагина
add_library(libobs SHARED IMPORTED GLOBAL)
set_target_properties(libobs PROPERTIES
  IMPORTED_IMPLIB "${OBS_LIB}"
  IMPORTED_IMPLIB_RELEASE "${OBS_LIB}"
  IMPORTED_IMPLIB_DEBUG "${OBS_LIB}"
  INTERFACE_INCLUDE_DIRECTORIES "${OBS_INCLUDE}")

add_subdirectory("${PLUGIN_SRC}" "${CMAKE_BINARY_DIR}/plugin")
