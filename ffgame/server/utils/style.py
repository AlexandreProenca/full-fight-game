#  -*- coding: utf-8 -*-
class Colors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


MARGEM = 58 * "*"
LINHA = 116 * "*" + "\n"


def cavera():
    return """
                         __________
                      .~#########%%;~.
                     /############%%;`\\
                    /######/~\/~\%%;,; \\
                   |#######\    /;;;;.,.|
                   |#########\/%;;;;;.,.|
          XX       |##/~~\####%;;;/~~\;,|       XX
        XX..X      |#|  o  \##%;/  o  |.|      X..XX
      XX.....X     |##\____/##%;\____/.,|     X.....XX
 XXXXX.....XX      \#########/\;;;;;;,, /      XX.....XXXXX
X |......XX%,.@      \######/%;\;;;;, /      @#%,XX......| X
X |.....X  @#%,.@     |######%%;;;;,.|     @#%,.@  X.....| X
X  \...X     @#%,.@   |# # # % ; ; ;,|   @#%,.@     X.../  X
 X# \.X        @#%,.@                  @#%,.@        X./  #
  ##  X          @#%,.@              @#%,.@          X   #
, "# #X            @#%,.@          @#%,.@            X ##
   `###X             @#%,.@      @#%,.@             ####'
  . ' ###              @#%.,@  @#%,.@              ###`"
    . ";"                @#%.@#%,.@                ;"` ' .
      '                    @#%,.@                   ,.
      ` ,                @#%,.@  @@                `
                          @@@  @@@\n\n"""


def logo():
    return """
______     _ _  ______ _       _     _     _____
|  ___|   | | | |  ___(_)     | |   | |   |  __ \\
| |_ _   _| | | | |_   _  __ _| |__ | |_  | |  \/ __ _ _ __ ___   ___
|  _| | | | | | |  _| | |/ _` | '_ \| __| | | __ / _` | '_ ` _ \ / _ \\
| | | |_| | | | | |   | | (_| | | | | |_  | |_\ \ (_| | | | | | |  __/
\_|  \__,_|_|_| \_|   |_|\__, |_| |_|\__|  \____/\__,_|_| |_| |_|\___|
                          __/ |
                         |___/

"""


def first_menu(TITULO):
    return f"""{MARGEM} {Colors.OKBLUE} {TITULO} {Colors.ENDC} {MARGEM[:-len(TITULO)]}\n
    {Colors.FAIL}
    1) PERSONAGEM    {99*'-'}{Colors.OKGREEN}
    2) ON-LINE USERS {99*'-'}{Colors.WARNING}
    3) SAIR          {99*'-'}{Colors.ENDC}
    {Colors.ENDC}
    {LINHA}
    Digite sua opção:"""


def char_set_menu(char, TITULO):
    return f"""{MARGEM} {Colors.OKBLUE} {TITULO} {Colors.ENDC} {MARGEM[:-len(TITULO)]}
    Voce tem {char.skill_points} pontos para distribuir entre os atributos do seu personagem, \nfique atento ao valor maximo de cada atributo\n
    {Colors.WARNING}
    Perfil           :{char.username}\n
    1) Nome          {char.name}{Colors.WARNING}
    2) Força         {char.p_atk}{Colors.WARNING}
    3) Defesa        {char.p_def}{Colors.WARNING}
    4) Agilidade     {char.agility}{Colors.WARNING}
    5) Raiva         {char.rage}{Colors.WARNING}
    6) Vitalidade    {char.hp}{Colors.ENDC}
    {LINHA}
    {Colors.OKBLUE}
    8) VOLTAR        {99*'*'}){Colors.ENDC}
    9) JOGAR         {99*'*'} {Colors.HEADER}
    10) HELP         {99*'*'}
    {Colors.ENDC}
    {LINHA}"""


def help_menu(TITULO):
    return f"""{MARGEM} {Colors.OKBLUE} {TITULO} {Colors.ENDC} {MARGEM[:-len(TITULO)]}{Colors.WARNING}
    (1) Nome       * Define o nome do seu personagem ***********************************************)
    (2) Força      * Define a foça bruta do seu golpe ****************************** MAX = 35  *****)
    (3) Defesa     * Define a defesa bruta contra golpes sofridos ****************** MAX = 35  *****)
    (4) Agilidade  * Melhora porcentagem de chance de desviar de golpes sofridos *** MAX = 5   *****)
    (5) Raiva      * Melhora porcentagem de chance de acertar golpes fatais ******** MAX = 5   *****)
    (6) Vitalidade * Define a quantidade de pontos de vida do seu personagem (HP)*** MAX = 150 *****)
    {Colors.ENDC}"""


def confirm_message(name):
    return f"Nome:{Colors.OKBLUE}{name}{Colors.ENDC}\nConfirma ? s/n? : "


welcome = f"{cavera()}\n {Colors.OKBLUE}\n {logo()}\n{Colors.ENDC}"
name_message = f"{Colors.ENDC}Digite seu Nome e pressione Enter ou {Colors.FAIL}Crt-c para Sair{Colors.ENDC}\n"

bye_message = f"{Colors.WARNING} Valeu por jogar, volte sempre =)\n Pressione Ctrl+] depois digite quit para sair do telnet\n  {Colors.ENDC}"
invalid_option = f"{Colors.FAIL}  Invalid Option\n {Colors.ENDC}"
