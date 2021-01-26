from ply import lex
import ply.yacc as yacc
import string
import re
import csv

 # LEX
tokens = (
    'TABLEO',
    'TRO',
    'THO',
    'THC',
    'TRC',
    'TDO',
    'TDC',
    'TABLEC',
    'WORD',
    'ANYTAGO',
    'ANYTAGC'
)

t_ignore = ' \t\n'
ident = r'[a-z]\w*'

t_TABLEO = r'<table.*?>'
t_TRO = r'<tr.*?>'
t_THO = r'<th.*?>'  
t_TRC = r'</tr>'
t_THC = r'</th>'
t_TDO = r'<td.*?>'
t_TDC = r'</td>'
t_TABLEC = r'</table>'


def t_ANYTAGO(t):
    r'<\s*[a-zA-Z]+.*?>'
    if re.match(t_TABLEO, t.value):
        t.type = 'TABLEO'
        return t
    elif re.match(t_TRO, t.value):
        t.type = 'TRO'
        return t
    elif re.match(t_THO, t.value):
        t.type = 'THO'
        return t
    elif re.match(t_TDO, t.value):
        t.type = 'TDO'
        return t
    return None


def t_ANYTAGC(t):
    r'</\s*[a-zA-Z]+.*?>'
    if re.match(t_TABLEC, t.value):
        t.type = 'TABLEC'
        return t
    elif re.match(t_TRC, t.value):
        t.type = 'TRC'
        return t
    elif re.match(t_THC, t.value):
        t.type = 'THC'
        return t
    elif re.match(t_TDC, t.value):
        t.type = 'TDC'
        return t
    return None


t_WORD = r' \s*[a-zA-Z0-9().,\-:;@#$%^&*\[\]\"\'+–/\/®°⁰!?{}|`~ ]+'


def t_error( t ):
  print("Invalid Token:",t.value[0])
  t.lexer.skip( 1 )


lexer = lex.lex()

 # YACC 
class Node:
    def parts_str(self):
        st = []
        for part in self.parts:
            st.append( str( part ) )
        return "\n".join(st)


    def __repr__(self):
        return self.type + ":\n\t" + self.parts_str().replace("\n", "\n\t")


    def add_parts(self, parts):
        self.parts += parts
        return self


    def __init__(self, type, parts):
        self.type = type
        self.parts = parts


    def to_list(self):
        tables = []
        if len(self.parts) > 0:
            for part in self.parts:
                if type(part) is Node:
                    tables.append(part.to_list())
                else:
                    tables.append(part)        
        return tables


def p_table(p):
    '''table :
             | table TABLEO tablebody TABLEC
             | word table word'''
    if len(p) == 1:
        p[0] = Node('tables',[])
    elif len(p) == 3:
        if p[1] == 'table':
            p[0] = p[1]
        else:
            p[0] = p[2]
    elif len(p) == 4:
        p[0] = p[2]
    else:
        if p[1] == None:
            p[1] == Node('tables',[])
        p[0] = p[1].add_parts([p[3]])


def p_tablebody(p):
    '''tablebody : 
                 | tablebody TRO bodycolumns TRC'''
    if len(p) > 1:
        if p[1] == None:
            p[1] = Node('table', [])
        p[0] = p[1].add_parts([p[3]])
    else:
        p[0] = Node('table', [])


def p_bodycolumns(p):
    '''bodycolumns : 
                   | bodycolumns TDO word TDC
                   | bodycolumns THO word THC
                   | bodycolumns TDO table TDC
                   | bodycolumns THO table THC'''
    if len(p) > 1:
        if p[1] == None:
            p[1] = Node('row',[])
        p[0] = p[1].add_parts([p[3]])


def p_word(p):
    '''word : 
            | word WORD'''
    if len(p) > 2:
        if p[1] == None:
            p[1] = ''
        p[0] = p[1]+p[2]
    elif len(p) ==2:
        p[0] = p[1]


def p_error(p):
     if p:
          print("Syntax error at token", p.type)
          # Just discard the token and tell the parser it's okay.
          parser.errok()
     else:
          print("Syntax error at EOF")


 # Write table to file
def save_to_file(data, filename):
    with open(filename, 'w') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        for row in data:
            line = []            
            for ro in row:
                if type(ro) is list and len(ro)>0:
                    save_to_file(ro[0], filename + '1')
                    continue
                line.append(ro)
            wr.writerow(line)

 # DATA
data = '''
<table class="infobox vevent" style="width:22em">
    <tbody>
        <tr>
            <th colspan="2" class="summary" style="text-align:center;font-size:125%;font-weight:bold;background-color: #eedd82;">Caldecott Medal</th>
        </tr>
        <tr><td colspan="2" style="text-align:center"><a href="/wiki/File:Caldecott_Medal.jpg" class="image"><img alt="Caldecott Medal.jpg" src="//upload.wikimedia.org/wikipedia/en/thumb/a/af/Caldecott_Medal.jpg/220px-Caldecott_Medal.jpg" decoding="async" width="220" height="106" srcset="//upload.wikimedia.org/wikipedia/en/thumb/a/af/Caldecott_Medal.jpg/330px-Caldecott_Medal.jpg 1.5x, //upload.wikimedia.org/wikipedia/en/a/af/Caldecott_Medal.jpg 2x" data-file-width="356" data-file-height="171"></a></td></tr>
        <tr><th scope="row" style="width: 33%;">Awarded for</th><td>"the most distinguished American <a href="/wiki/Picture_book" title="Picture book">picture book</a> for children"</td></tr>
        <tr><th scope="row" style="width: 33%;">Country</th><td class="location">United States</td></tr>
        <tr>
            <th scope="row" style="width: 33%;">Presented by</th>
            <td class="attendee"><a href="/wiki/Association_for_Library_Service_to_Children" title="Association for Library Service to Children">Association for Library Service to Children</a>, a division of the <a href="/wiki/American_Library_Association" title="American Library Association">American Library Association</a></td>
        </tr>
        <tr><th scope="row" style="width: 33%;">First awarded</th><td>1938<span class="noprint">; 83&nbsp;years ago</span><span style="display:none">&nbsp;(<span class="bday dtstart published updated">1938</span>)</span></td></tr>
        <tr><th scope="row" style="width: 33%;">Website</th><td><span class="url"><a rel="nofollow" class="external text" href="http://ala.org/alsc/caldecott">ala<wbr>.org<wbr>/alsc<wbr>/caldecott</a></span></td></tr>
    </tbody>
</table>
<wlef></wlef>
<table style="width:100%">
  <tr>
    <td>Jill</td>
    <td>Smith</td>
    <td>50</td>
  </tr>
  <tr>
    <td>Eve</td>
    <td>Jackson</td>
    <td>94</td>
  </tr>  
  <tr>
    <td>dfl <a>John</a><a>John</a><a>John</a></td>
    <td>Doe</td>
    <td>80</td>
    <td>
        <table>
            <tr>
                <th class = "dsfgs" >
                    First name
                </th>
                <th>Lastname</th> 
                <th>Age</th>
            </tr>
        </table>
    </td>
  </tr>
</table>
'''

 # RUN
 
 # Reduce all consecutive spaces in data to 1
print('\nNormalized data:\n')
data = ' '.join(data.split())
print(data)

 # Display all tokens in order as they appear
print('\nList of tokens:\n')
lexer.input(data)
for l in lexer:
    print(l)

print('\nTree of tables:\n')
yacc.yacc()
tables_tree = yacc.parse(data)
print(tables_tree)

 # Convert tree to list
tables_tree_list = tables_tree.to_list()

 # Write all tables to separate files
print('\nTables as lists:\n')
count=0
for part in tables_tree_list:
    print(part,'\n\n')
    save_to_file(part,'table' + str(count))
    count += 1
