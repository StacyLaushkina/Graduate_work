import flask, flask.views, os, nltk
from flask import url_for

app = flask.Flask(__name__)
#Do not do this
app.secret_key = "some_secret"
CSRF_ENABLED = True

class View(flask.views.MethodView):
    def get(selfself):
        return flask.render_template('parse.html')

class Developer_View(flask.views.MethodView):
    def get(selfself):
        return flask.render_template('developer_information.html')

class Other_View(flask.views.MethodView):
    def get(selfself):
        return flask.render_template('other.html')

class Start_View(flask.views.MethodView):
    def get(self):
        return flask.render_template('index.html')
    def post(self):

        InitFlag = 0
        TomitaFlag = 0
        if (flask.request.form['tomita_expression'] != 'null_value'): TomitaFlag = 1

        if ((flask.request.form['LookAt'] == 'TRUE')&(not(TomitaFlag))):
            flask.flash("Your library:")
            my_library = read_my_library()
            InitFlag = 1
            i = 0
            last_i = len(my_library)
            while(i<last_i):
                flask.flash(my_library[i])
                i = i+1

        if ((flask.request.form['expression'] != '')&(not(TomitaFlag))):
            # if we haven't read my_library yet
            if (not(InitFlag)):
                my_library = read_my_library()
                InitFlag = 1
            result = parse(my_library)
            flask.flash('The results of the search:')
            if (result != []):
                i = 0
                last_i = len(result)
                while(i<last_i):
                    flask.flash(result[i])
                    i = i+1
            else: flask.flash('Program did not found any sentences with your word')

        if ((flask.request.form['new_word'] != '')&(not(TomitaFlag))):
            # if we haven't read my_library yet
            if (not(InitFlag)):
                my_library = read_my_library()
                InitFlag = 1
            tmp = enter_new_word(my_library)
            if (tmp):  flask.flash('New word was successfully added!')
            else: flask.flash('This word already exist in library')

        if ( (not(InitFlag))& (not(TomitaFlag)) | (flask.request.form['tomita_expression'] == '') ):
            flask.flash('Please enter some value')

        if ((TomitaFlag)&(flask.request.form['tomita_expression']!='')):
            wtf = open('input.txt','w')
            expr = flask.request.form['tomita_expression']
            expr = expr.encode('utf-8')
            wtf.write(expr)
            wtf.close()

            res_flag = 0
            if (flask.request.form['tomita_sphere_Bas'] == 'TRUE'):
                flask.flash('Basic facts:')
                os.system('./tomita-linux32 configB.proto')
                # read result of tomita
                rtf = open('facts.txt','r')
                read_data = str(rtf.read())
                rtf.close()
                # transform to pretty format
                read_data = read_data.rjust(1,'\n')
                q = read_data.split('\n')
                i = 0
                last_i = len(q)
                # flag for existing of the result
                while (i<last_i):
                    if (q[i] == '\tBasicFact'):
                        res_flag = 1
                        res = q[i-1].decode('utf-8')
                        flask.flash (res)
                    i = i+1
                if (not(res_flag)):
                    flask.flash('Program did not found any basic facts in your text')

            res_flag = 0
            if (flask.request.form['tomita_sphere_Fam'] == 'TRUE'):
                flask.flash('Family facts:')
                os.system('./tomita-linux32 configF.proto')
                # read result of tomita
                rtf = open('facts.txt','r')
                read_data = str(rtf.read())
                rtf.close()
                # transform to pretty format
                read_data = read_data.rjust(1,'\n')
                q = read_data.split('\n')
                i = 0
                last_i = len(q)
                # flag for existing of result
                while (i<last_i):
                    if (q[i] == '\tFamilyFact'):
                        res_flag = 1
                        res = q[i-1].decode('utf-8')
                        flask.flash (res)
                    i = i+1
                if (not(res_flag)):
                    flask.flash('Program did not found any Family facts in your text')

            res_flag = 0
            if (flask.request.form['tomita_sphere_Liv'] == 'TRUE'):
                flask.flash('Facts about live:')
                os.system('./tomita-linux32 configA.proto')
                # read result of tomita
                rtf = open('facts.txt','r')
                read_data = str(rtf.read())
                rtf.close()
                # transform to pretty format
                read_data = read_data.rjust(1,'\n')
                q = read_data.split('\n')
                i = 0
                last_i = len(q)
                # flag for existing of result
                while (i<last_i):
                    if (q[i] == '\tActionFact'):
                        res_flag = 1
                        res = q[i-1].decode('utf-8')
                        flask.flash (res)
                    i = i+1
                if (not(res_flag)):
                    flask.flash('Program did not found any Action facts in your text')

        if (not(TomitaFlag)):return flask.render_template('parse.html')
        else:return flask.render_template('tomita_parser.html')

class Tomita_view(flask.views.MethodView):
    def get(selfself):
        return flask.render_template('tomita_parser.html')

def read_my_library():
    rf = open('my_library','r')
    read_data = str(rf.read())
    rf.close()
    # transform data to useful format
    my_library = read_data.split(', ')
    i = 0
    last_i = len(my_library)
    while (i<last_i):
        my_library[i] = my_library[i].split(' ')
        i = i+1
    return my_library

def parse(my_library):
    from nltk.tag.stanford import NERTagger
    st = NERTagger('stanford-ner/classifiers/english.muc.7class.distsim.crf.ser.gz',
                   'stanford-ner/stanford-ner.jar')
    sent = nltk.sent_tokenize(flask.request.form['expression'])
    words=range(len(sent))
    res = []
    i = 0
    last_i = len(sent)
    if (flask.request.form['search_word_tag'] == 'NULL'): tag_flag = 0
    else: tag_flag = 1
    while (i<last_i):
        words[i] = st.tag(nltk.word_tokenize(sent[i]))
        j=0
        last_j = len(words[i])
        # if word is in the sentence
        flag1 = 0
        # if sentence contains  weighty words
        flag2 = 0
        # if tag is in sentence
        flag3 = 0
        tag = 0
        while (j<last_j):
            # Stanford library
            if (words[i][j][1]<> 'O'):
                flag2 = 1
                if ((tag_flag)&(words[i][j][1] == flask.request.form['search_word_tag'])):flag3 = 1
            else:
                #My_library
                tag = search_in_new_library(my_library,words[i][j][0])
                if (tag): flag2 = 1
                if ((tag_flag)&(tag == flask.request.form['search_word_tag'])): flag3 = 1
            if (words[i][j][0] == flask.request.form['search']): flag1 = 1
            j=j+1
        # searching without tag
        if ((flag1)&(flag2)&(not(tag_flag))):
            res.append(sent[i])
        #search with tag
        if ((flag1)&(flag2)&(flag3)&(tag_flag)):
            res.append(sent[i])
        i = i+1
    return res

# function returns tag of x in my_library or null
def search_in_new_library(my_library, x):
    i=0
    tag = 0
    last_i = len(my_library)
    while (i<last_i):
        if (x == my_library[i][0]): tag = my_library[i][1]
        i=i+1
    return tag

def write_to_file(my_library):
    wf = open('my_library','a')
    if (my_library[0][0] == ''): new1 =  flask.request.form['new_word'] + ' ' + flask.request.form['new_word_tag']
    else: new1 = ', ' + flask.request.form['new_word'] + ' ' + flask.request.form['new_word_tag']
    wf.write(new1)

def enter_new_word(my_library):
    from nltk.tag.stanford import NERTagger
    st = NERTagger('stanford-ner/classifiers/english.muc.7class.distsim.crf.ser.gz',
                   'stanford-ner/stanford-ner.jar')
    new = st.tag ([flask.request.form['new_word']])
    # is new word already exist in Stanford library?
    if (new[0][1] <> 'O'): return 0
    # is new word already exist in My_library?
    if (search_in_new_library(my_library, new[0][0])): return 0
    write_to_file(my_library)
    return 1


app.add_url_rule('/',view_func = Start_View.as_view('start'), methods = ['GET','POST'])
app.add_url_rule('/parse',view_func = View.as_view('parse'), methods = ['GET','POST'])
app.add_url_rule('/start_page',view_func = Start_View.as_view('index'), methods = ['GET','POST'])
app.add_url_rule('/other',view_func = Other_View.as_view('other'), methods = ['GET','POST'])
app.add_url_rule('/tomita_parser',view_func = Tomita_view.as_view('tomita'), methods = ['GET','POST'])
app.add_url_rule('/developer_information',view_func = Developer_View.as_view('developer_information'), methods = ['GET','POST'])

app.debug = True
app.run()
