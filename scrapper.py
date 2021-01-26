from ply import lex
import ply.yacc as yacc
import string
import re

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
    # print('LOOK: ', t.value)
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
        # if self.type == 'word':
            # return self.parts[0]
        return self.type + ":\n\t" + self.parts_str().replace("\n", "\n\t")


    def add_parts(self, parts):
        self.parts += parts
        return self


    def __init__(self, type, parts):
        self.type = type
        self.parts = parts
   
   
def p_table(p):
    '''table :
             | table TABLEO tablebody TABLEC
             | word table word'''
    if len(p) == 1:
        p[0] = Node('table',[])
    elif len(p) == 3:
        if p[1] == 'table':
            p[0] = p[1]
        else:
            p[0] = p[2]
    elif len(p) == 4:
        p[0] = p[2]
    else:
        if p[1] == None:
            p[1] == Node('table',[])
        p[0] = p[1].add_parts([p[3]])
    # print(p[0])


def p_tablebody(p):
    '''tablebody : 
                 | tablebody TRO bodycolumns TRC'''
    if len(p) > 1:
        if p[1] == None:
            p[1] = Node('body', [])
        p[0] = p[1].add_parts([p[3]])
    else:
        p[0] = Node('body', [])
    
    
def p_bodycolumns(p):
    '''bodycolumns : 
                   | bodycolumns TDO word TDC
                   | bodycolumns THO word THC'''
    if len(p) > 1:
        if p[1] == None:
            p[1] = Node('content',[])
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
    <th class = "dsfgs" >
        First name
    </th>
    <th>Lastname</th> 
    <th>Age</th>
  </tr>
  <tr>
    <td> ;sodhbjfn (&^*$&#Jill</td>
    <td>Smith</td>
    <td>50</td>
  </tr>
  <tr>
    <th>Eve</th>
    <th>Jackson</th>
    <th>94</th>
  </tr>
  <tr>
    <td>dfl <a>John</a><a>John</a><a>John</a></td>
    <td>Doe</td>
    <td>80</td>
   
  </tr>
</table>
'''

data = ' '.join(data.split())
print(data)

lexer.input(data)
for l in lexer:
    print(l)

yacc.yacc()
print(yacc.parse(data).__repr__)