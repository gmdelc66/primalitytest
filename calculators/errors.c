/*
This file is part of Alpertron Calculators.

Copyright 2015 Dario Alejandro Alpern

Alpertron Calculators is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Alpertron Calculators is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Alpertron Calculators.  If not, see <http://www.gnu.org/licenses/>.
*/

#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include "bignbr.h"
#include "expression.h"

int expressionNbr;
void textError(char *ptrOutput, enum eExprErr rc)
{
  switch (rc)
  {
  case EXPR_NUMBER_TOO_LOW:
    strcpy(ptrOutput, lang ? "Número muy pequeño" : "Number too low");
    break;
  case EXPR_NUMBER_TOO_HIGH:
    strcpy(ptrOutput, lang ? "Número muy grande (más de 10000 dígitos)" :
      "Number too high (more than 10000 digits)");
    break;
  case EXPR_INTERM_TOO_HIGH:
    strcpy(ptrOutput, lang ? "Número intermedio muy grande (más de 20000 dígitos" :
      "Intermediate number too high (more than 20000 digits)");
    break;
  case EXPR_DIVIDE_BY_ZERO:
    strcpy(ptrOutput, lang ? "División por cero" : "Division by zero");
    break;
  case EXPR_PAREN_MISMATCH:
    strcpy(ptrOutput, lang ? "Error de paréntesis" : "Parenthesis mismatch");
    break;
  case EXPR_SYNTAX_ERROR:
    if (lang)
    {
      strcpy(ptrOutput, "Error de sintaxis");
      if (expressionNbr > 0)
      {
        ptrOutput += strlen(ptrOutput);
        strcpy(ptrOutput, " en la expresión ");
        ptrOutput += strlen(ptrOutput);
        *ptrOutput++ = (char)(expressionNbr + '0');
        *ptrOutput++ = 0;
      }
    }
    else
    {
      strcpy(ptrOutput, "Syntax error");
      if (expressionNbr > 0)
      {
        ptrOutput += strlen(ptrOutput);
        strcpy(ptrOutput, " in expression #");
        ptrOutput += strlen(ptrOutput);
        *ptrOutput++ = (char)(expressionNbr + '0');
        *ptrOutput++ = 0;
      }
    }
    break;
  case EXPR_TOO_MANY_PAREN:
    strcpy(ptrOutput, lang ? "Demasiados paréntesis" : "Too many parenthesis");
    break;
  case EXPR_INVALID_PARAM:
    strcpy(ptrOutput, lang ? "Parámetro inválido" : "Invalid parameter");
    break;
  case EXPR_ARGUMENTS_NOT_RELATIVELY_PRIME:
    strcpy(ptrOutput, lang ? "MCD de los argumentos no es 1" : "GCD of arguments is not 1");
    break;
  case EXPR_BREAK:
    strcpy(ptrOutput, lang ? "Detenido por el usuario" : "Stopped by user");
    break;
  case EXPR_VAR_OR_COUNTER_REQUIRED:
    if (lang)
    {
      strcpy(ptrOutput, "La expresión ");
      ptrOutput += strlen(ptrOutput);
      *ptrOutput++ = (char)(expressionNbr + '0');
      strcpy(ptrOutput, " debe incluir la variable <var>x</var> y/o el contador <var>c</var>");
    }
    else
    {
      strcpy(ptrOutput, "Expression #");
      ptrOutput += strlen(ptrOutput);
      *ptrOutput++ = (char)(expressionNbr + '0');
      strcpy(ptrOutput, " must include the variable <var>x</var> and/or the counter <var>c</var>");
    }
    break;
  default:
    break;
  }
}
