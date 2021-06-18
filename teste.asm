
; constantes
SYS_EXIT equ 1
SYS_READ equ 3
SYS_WRITE equ 4
STDIN equ 0
STDOUT equ 1
True equ 1
False equ 0

segment .data

segment .bss  ; variaveis
  res RESB 1

section .text
  global _start

print:  ; subrotina print

  PUSH EBP ; guarda o base pointer
  MOV EBP, ESP ; estabelece um novo base pointer

  MOV EAX, [EBP+8] ; 1 argumento antes do RET e EBP
  XOR ESI, ESI

print_dec: ; empilha todos os digitos
  MOV EDX, 0
  MOV EBX, 0x000A
  DIV EBX
  ADD EDX, '0'
  PUSH EDX
  INC ESI ; contador de digitos
  CMP EAX, 0
  JZ print_next ; quando acabar pula
  JMP print_dec

print_next:
  CMP ESI, 0
  JZ print_exit ; quando acabar de imprimir
  DEC ESI

  MOV EAX, SYS_WRITE
  MOV EBX, STDOUT

  POP ECX
  MOV [res], ECX
  MOV ECX, res

  MOV EDX, 1
  INT 0x80
  JMP print_next

print_exit:
  POP EBP
  RET

; subrotinas if/while
binop_je:
  JE binop_true
  JMP binop_false

binop_jg:
  JG binop_true
  JMP binop_false

binop_jl:
  JL binop_true
  JMP binop_false

binop_false:
  MOV EBX, False
  JMP binop_exit
binop_true:
  MOV EBX, True
binop_exit:
  RET

_start:

  PUSH EBP ; guarda o base pointer
  MOV EBP, ESP ; estabelece um novo base pointer

  ; codigo gerado pelo compilador

PUSH DWORD 0
PUSH DWORD 0
PUSH DWORD 0
PUSH DWORD 0
PUSH DWORD 0
MOV EBX, False
MOV [EBP-False], EBX
MOV EBX, 1
MOV [EBP-1], EBX
MOV EBX, 4
MOV EBX, 4
MOV EBX, 5
IMUL EBX
MOV EBX, EAX
ADD EAX, EBX
MOV EBX, EAX
MOV [EBP-24], EBX
MOV EBX, [EBP -24]
MOV EBX, -24
PUSH EBX
CALL print
POP EBX
MOV EBX, [EBP -False]
MOV EBX, !False
PUSH EBX
CALL print
POP EBX
MOV EBX, [EBP -1]
MOV EBX, [EBP -24]
CMP EAX, EBX
CALL binop_jl
MOV [EBP-True], EBX
MOV EBX, [EBP -True]
MOV EBX, [EBP -24]
MOV EBX, [EBP -1]
CMP EAX, EBX
CALL binop_jl
MOV EBX, [EBP -1]
MOV EBX, [EBP -24]
CMP EAX, EBX
CALL binop_jl
OR EAX, EBX
MOV EBX, EAX
OR EAX, EBX
MOV EBX, EAX
CMP EBX, False
JE ELSE_55
MOV EBX, 10
PUSH EBX
CALL print
POP EBX
MOV EBX, [EBP -1]
MOV EBX, 1
ADD EAX, EBX
MOV EBX, EAX
MOV [EBP-2], EBX
JMP ENDBLOCK_55
ELSE_55
ENDBLOCK_55
MOV EBX, 1
MOV EBX, 1
CMP EAX, EBX
CALL binop_jl
CMP EBX, False
JE ELSE_62
MOV EBX, 99
PUSH EBX
CALL print
POP EBX
JMP ENDBLOCK_62
ELSE_62
ENDBLOCK_62
LOOP_76:
MOV EBX, 2
MOV EBX, 2
CMP EAX, EBX
CALL binop_jl
MOV EBX, [EBP -2]
MOV EBX, 10
CMP EAX, EBX
CALL binop_jl
OR EAX, EBX
MOV EBX, EAX
CMP EBX, False
JE EXIT_76
MOV EBX, [EBP -2]
MOV EBX, 1
ADD EAX, EBX
MOV EBX, EAX
MOV [EBP-3], EBX
JMP LOOP_76:
EXIT_76:
MOV EBX, 5
PUSH EBX
CALL print
POP EBX

POP EBP
MOV EAX, 1
INT 0x80
