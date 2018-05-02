# -*- coding=utf-8 -*-
#!/usr/bin/env python

import click
import sklearn
from os import walk, makedirs, linesep
from os.path import join,relpath, exists, dirname
from multiprocessing import  Pool
from shutil import copyfile
import time
import logging
from logging import info as _i, debug as _d
import random
import extracttfidf
import pandas as pd
from keras.preprocessing import text
from sklearn.feature_extraction.text import TfidfVectorizer
from functools import wraps
import scipy.sparse
import chardet
from feature_extractor import FeatureExtractor
#from ipdb import set_trace
import numpy as np
from sklearn.ensemble import ExtraTreesClassifier
import matplotlib.pyplot as plt
from jinja2 import Template
from configparser import ConfigParser


def src_to_normalize_(params):
    # TODO: extract text directly 
    def src_to_normalize(src,dst):
        if not exists(dirname(dst)):
            makedirs(dirname(dst))
        fextractor = FeatureExtractor('pysie.cfg')
        logging.debug(src)
        with open(src, 'rb') as src_file:
            src_data = src_file.read()
        with open(dst, 'wb') as dst_file:
            if len(src_data) > 20:
                enc = chardet.detect(src_data)
                encoding = enc['encoding'] if enc and enc['encoding'] else 'utf-8'
                src_data = src_data.decode(encoding, errors='ignore')
                dst_body = fextractor.get_jsvbs_content(src_data)
                if dst_body:
                    dst_file.write(dst_body.encode('utf-8', errors = 'ignore'))
    src_to_normalize(params[0], params[1])


logging.basicConfig(
     level=logging.DEBUG, 
     format= '[%(asctime)s] {%(filename)10s:%(lineno)d} %(levelname)s - %(message)s',
     datefmt='%H:%M:%S'
 )

def profile(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        started_at = time.time()
        _d('Start ' + func.__name__)
        _d('args = {0}'.format(args))
        _d('kwargs = {0}'.format(kwargs))
        result = func(*args, **kwargs)
        logging.info('End {0}, used time is {1}'.format(func.__name__, time.time() - started_at))
        return result
    return wrap

g_sie_config = None
def get_sie_config():
    global g_sie_config
    if not g_sie_config:
        raise NotImplementedError
    return g_sie_config
def _cfg(*args, **kwargs):
    return get_sie_config().get(*args, **kwargs)

def get_path(name):
    workspace_root = _cfg('path', 'workspace_root')
    return join(workspace_root, _cfg('job', 'job_id'), _cfg('path',name))
_path = get_path
def init_sie_config(cfg_path):
    global g_sie_config
    if g_sie_config is not None:
        assert False, 'sie has been initialized!'
    g_sie_config = ConfigParser()
    g_sie_config.read(cfg_path)

def dataframe_2_file(df, p):
    df.to_csv(p)

def file_2_dataframe(p):
    return pd.read_csv(p)

def ensure_dir(p):
    if not exists(p):
        makedirs(p)

@click.command()
@click.option('--job-id', default = None, help='')
@profile
def create_job(job_id):
    '''Create a new job id and prepare the folder related with job'''
    if job_id is None:
        job_id = time.strftime('%b%d%Y_%H_%M_%S', time.gmtime())
    _i('job_id={0}'.format(job_id))
    workspace_root = _cfg('path', 'workspace_root')
    workspace_path = join(workspace_root, job_id)
    ensure_dir(workspace_path)
    return job_id

@click.command()
@click.option('--tfidf-martrix-prefix', help='path of tfidf martrix npz file')
@profile
def sort_tfidf(tfidf_martrix_prefix):
    # list of text documents
    tfidf_martrix = scipy.sparse.load_npz(tfidf_martrix_prefix + '.npz')
    #tfidf_df = pd.DataFrame(tfidf_martrix)
    tfidf_feature_argmax = np.argmax(tfidf_martrix, axis=0)
    print(tfidf_martrix.shape)
    #get the max tfidf value of every keyword
    #TODO: optimize me
    tfidf_feature_max = list(map(lambda v: (tfidf_martrix[v[1], v[0]],), enumerate(tfidf_feature_argmax.flat)))
    df = pd.DataFrame.from_records(tfidf_feature_max, columns = [ 'max_tfidf'])
    dataframe_2_file(df, tfidf_martrix_prefix + '.maxtfidf.csv')
    k = 200
    #get the index of top k keyword, [0.3,0.1,0.23]->[1,3,2]
    #max_index = tfidf_feature_max.argsort()[-2:][::-1]
    keyword_csv_path = tfidf_martrix_prefix + '.keyword.csv'
    
    df_keyword_index = file_2_dataframe(keyword_csv_path)
    print(df_keyword_index)
    df_keyword_index = df_keyword_index.sort_values(by=['index'])
    print('df_keyword_index.shape=' + str(df_keyword_index.shape))
    print('tfidf_feature_max.shape=' + str(df.shape))
    df_keyword_index = pd.concat( [df_keyword_index, df], axis=1)
    df_keyword_index = df_keyword_index.sort_values(by=['max_tfidf'])
    dataframe_2_file(df_keyword_index, tfidf_martrix_prefix + '.max.csv')

def tokenizer(doc):
    max_word_length = 20
    min_word_length = 3
    words = filter(lambda w: min_word_length <= len(w) <= max_word_length,
                            text.text_to_word_sequence(doc,
                                filters='!"#$%&()*+,-./:;<=>?@[\\]^_`\'{|}~\t\n\r',
                                lower=True,
                                split=" "))
    words = map(lambda w: w.strip(), words)  
    return words

@click.command()
@click.option('--sample-path-list', help='Training sample path, Note: validation sample should be excluded!')
@click.option('--result-prefix', default="tfidf_vectorizer.list", help='Result path')
@profile
def tfidf_vectorizer(sample_path_list, result_prefix):
    #get file 
    # list of text documents
    # (sample_path, label)
    df = file_2_dataframe(sample_path_list)
    # create the transform
    # TODO: add a progress indicator in tokenizer
    vectorizer = TfidfVectorizer(input='filename', tokenizer=tokenizer, decode_error='ignore')
    # tokenize and build vocab
    tfidf_martrix = vectorizer.fit_transform(df['sample_path'])
    martrix_path = result_prefix + '.npz'
    scipy.sparse.save_npz(martrix_path, tfidf_martrix)
    #save vocalbulary
    df_vocabulary = pd.DataFrame.from_records(list(vectorizer.vocabulary_.items()), columns = ['keyword', 'index'])
    keyword_csv_path = result_prefix + '.keyword.csv'
    dataframe_2_file(df_vocabulary,keyword_csv_path)
    print('fit samples compilete')

@click.command()
@click.option('--cfg-path', default='pysie.cfg', help='')
@click.option('--keyword-with-importance-path', default = 'df_keyword_with_importance.csv')
@click.option('--script-keyword-yar-template-path', default = 'script_keyword.yar.tmpl')
@click.option('--k', default=300, help='')
@profile
def build_script_keyword_yar_rule(cfg_path, keyword_with_importance_path, script_keyword_yar_template_path, k):
    script_keyword_yar_path = _path('script_keyword_yar')
    #select top keywords
    df_keyword = file_2_dataframe(keyword_with_importance_path)
    _d('df_keyword.shape={0}'.format(df_keyword.shape))
    #render template
    tmpl = '''
    {% for keyword in keywords %}
    rule keyword_{{ keyword.name }}{
    meta:
        index="{{loop.index0}}"
        TFIDF="0"
    strings:
        $s="{{ keyword.name }}" fullword nocase
    condition:
        $s
    }
    {% endfor %}
    '''
    template = Template(tmpl)
    df_k_keyword = df_keyword.sort_values(by=['importance'])[-k:][::-1]
    keywords = list(map(lambda k: { 'name': k[1]['keyword'] }, df_k_keyword.iterrows()))
    #filter out keyword with non-ascii
    #TODO: move this logic to word process
    keywords = filter(lambda s:  all(ord(c) < 128 for c in s['name']), keywords)
    with open(script_keyword_yar_path, 'w') as f:
        f.write(template.render(keywords = keywords))

@click.command()
@click.option('--file-list-path', default='train_test.list.csv', help='')
@click.option('--tfidf-martrix-path', default="tfidf_vectorizer.list.npz", help='')
@click.option('--keyword-list-path', default="tfidf_vectorizer.list.npz.keyword.csv", help='')
@click.option('--keyword-sort-by-importance-path', default="keyword_sort_by_importance.csv", help='')
@click.option('--k', default=300, help='')
@click.option('--n-estimators', default=5, help='')
@profile
def select_k_max(file_list_path, tfidf_martrix_path, keyword_list_path, keyword_sort_by_importance_path, k, n_estimators):
    df_file_list = file_2_dataframe(file_list_path)
    _i('df_file_list.shape={0}'.format(df_file_list.shape))
    df_tfidf_martrix = scipy.sparse.load_npz(tfidf_martrix_path)
    _i('df_tfidf_martrix.shape={0}'.format(df_tfidf_martrix.shape))
    df_keyword = file_2_dataframe(keyword_list_path)
    #_i('df_keyword.shape.before sort={0}'.format(df_keyword))
    #dataframe_2_file(df_keyword, 'df_keyword_before_sort.csv')
    df_keyword = df_keyword.sort_values(by= ['index'])
    df_keyword = df_keyword.reset_index(drop = True)
    _i('df_keyword.shape={0}'.format(df_keyword.shape))

    #dataframe_2_file(df_keyword, 'df_keyword.csv')
    label = (df_file_list['label'] == 'malicious').astype(int)
    #_i('label.shape={0}'.format(label.shape))    
    forest = ExtraTreesClassifier(n_estimators=n_estimators, random_state=0)
    forest.fit(df_tfidf_martrix, label)
    importances = forest.feature_importances_
    # not used
    # std = np.std([tree.feature_importances_ for tree in forest.estimators_],
    #          axis=0)
    df_importance = pd.DataFrame(importances, columns = ['importance'])
    #dataframe_2_file(df_importance, 'df_importance.csv')
    #_d('df_importance={0}'.format(df_importance))
    df_keyword = pd.concat([df_keyword, df_importance], axis = 1)
    dataframe_2_file(df_keyword, keyword_sort_by_importance_path)
    #_d('df_keyword={0}'.format(df_keyword.iloc[[1966580]]))
    df_keyword_sort_by_importance = df_keyword.sort_values(by=['importance'])
    
    _d('df_keyword_sort_by_importance={0}'.format(df_keyword_sort_by_importance[-100:][::-1]))
    # we can use below code to verify above result
    # indices = np.argsort(importances)[::-1]
    # print(indices[:10])
    # Print the feature ranking
    # print("Feature ranking:")
    # for f in range(k):
    #     print("%d. feature %d, %s (%f)" % (f + 1, indices[f], df_keyword[df_keyword['index'] == indices[f]]['keyword'].values[0], importances[indices[f]]))
    
@click.command()
@click.option('--cfg-path', default='pysie.cfg', help='')
@click.option('--sample-path-list', help='Training sample path, Note: validation sample should be excluded!')
@click.option('--result-path', default="tfidf_vectorizer.list", help='Result path')
@click.option('--select-type', help='Set type of select, default is tfidf')
@profile
def count_vectorizer(cfg_path, sample_path_list, result_path = None, select_type='tfidf'):
    #get file 
    # list of text documents
    # (sample_path, label)
    df = file_2_dataframe(sample_path_list)
    # create the transform
    # TODO: add a progress indicator in tokenizer
    vectorizer = TfidfVectorizer(input='filename', tokenizer=tokenizer, decode_error='ignore')
    # tokenize and build vocab
    tfidf_martrix = vectorizer.fit_transform(df['sample_path'])
    martrix_path = result_path + '.npz'
    scipy.sparse.save_npz(martrix_path, tfidf_martrix)
    #save vocalbulary
    df_vocabulary = pd.DataFrame.from_records(list(vectorizer.vocabulary_.items()), columns = ['keyword', 'index'])
    keyword_csv_path = martrix_path + '.keyword.csv'
    dataframe_2_file(df_vocabulary,keyword_csv_path)
    print('fit samples compilete')


@click.command()
@click.option('--sample-path', help='Training sample path, Note: validation sample should be excluded!')
@click.option('--normalized-sample-path', default="normalize_cache", help='Result path')
@profile
def normalize_sample(sample_path, normalized_sample_path):
    '''convert encoding to utf8
       extract js
    '''
    file_list = []    
    for root, dirs, files in walk(sample_path, topdown=False):
        for name in files:
            path = join(root, name)
            file_list.append(path)
    p = Pool()
    p.map(src_to_normalize_, [ (x, join(normalized_sample_path, relpath(x, sample_path))) for x in file_list])
    
@click.command()
@click.option('--sample-path', help='Training sample path, Note: validation sample should be excluded!')
@click.option('--file-list-path', default='file_list.list', help='Result path')
@profile
def to_file_list(sample_path, file_list_path):
    file_list = []
    for root, dirs, files in walk(sample_path, topdown=False):
        for name in files:
            path = join(root, name)
            file_list.append((path, 'malicious' if path.find('mal_set')!=-1 else 'normal'))
    df = pd.DataFrame.from_records(file_list, columns = [ 'sample_path', 'label'])
    with open(file_list_path, 'w') as w:
        w.writelines(x + '\n' for x in df['sample_path'])    
    dataframe_2_file(df, file_list_path + '.csv')
    
def sync_copy_file(src,dst):
    if not exists(dirname(dst)):
        makedirs(dirname(dst))
    copyfile(src, dst)
def sync_copy_file_(params):
    sync_copy_file(params[0], params[1])

@click.command()
@click.option('--sample-path', help='Training sample path, Note: validation sample should be excluded!')
@click.option('--file-list-path', default='file_list.list', help='Result path')
@click.option('--output-path', default='output', help='Result path')
def split_files(sample_path, file_list_path, output_path, rate=0.6):
    with open(file_list_path) as f_list:
        file_list = [x.strip() for x in f_list.readlines()]
    p = Pool()
    secure_random = random.SystemRandom()
    file_list_1_hit = set(secure_random.sample(xrange(len(file_list)), int(len(file_list) * rate)))
    file_list_1 = [ file_list[x] for x in file_list_1_hit ]
    file_list_2 = [ file_list[x] for x in xrange(len(file_list)) if x not in file_list_1_hit]
    p.map(sync_copy_file_, [ (x, join(output_path,'training', relpath(x, sample_path))) for x in file_list_1])
    p.map(sync_copy_file_, [ (x, join(output_path,'validataion', relpath(x, sample_path))) for x in file_list_2]) 

@click.command()
@click.pass_context
@profile
def group_sample_2_text(ctx):
    training_file_path = get_sie_config().get('sample', 'training_file_path')
    #convert coding to utf8, extract text from sample and cache the result in normalized_sample_path    
    normalize_sample_args = {'sample_path' : training_file_path
                            , 'normalized_sample_path': _path('normalized_sample_path')}
    ctx.invoke(normalize_sample, **normalize_sample_args)
    to_file_lsit_args = { "sample_path": normalize_sample_args['normalized_sample_path']
                        , 'file_list_path' : _path('normalized_sample_path_list') }
    ctx.invoke(to_file_list, **to_file_lsit_args)

@click.command()
@click.pass_context
def group_build_srcipt_keywords_yar(ctx):
    #tfidf_vectorizer
    tfidf_vectorizer_args = { 'sample_path_list': _path('normalized_sample_path_list') + '.csv' #use csv version here
                            , 'result_prefix': _path('tfidf_prefix')}
    ctx.invoke(tfidf_vectorizer, **tfidf_vectorizer_args)
    #sort tfidf
    sort_tfidf_args = { 'tfidf_martrix_prefix': _path('tfidf_prefix')}
    ctx.invoke(sort_tfidf, **sort_tfidf_args)    
    #select k max
    #file_list_path, tfidf_martrix_path, keyword_list_path, k, n_estimators
    select_k_max_args = { 'file_list_path': _path('normalized_sample_path_list') + '.csv'
                          , 'tfidf_martrix_path': _path('tfidf_prefix') + '.npz'
                          , 'keyword_list_path': _path('tfidf_prefix') + '.keyword.csv'
                          , 'keyword_sort_by_importance_path': _path('keyword_sort_by_importance_path')}
    ctx.invoke(select_k_max, **select_k_max_args)    
    #build script yar
    #keyword_with_importance_path, script_keyword_yar_template_path, k
    build_script_keyword_yar_rule_args = { 'keyword_with_importance_path': _path('keyword_sort_by_importance_path')
                                            ,'k': int(_cfg('job','script_keyword_number'))}
    ctx.invoke(build_script_keyword_yar_rule, **build_script_keyword_yar_rule_args)

@click.group()
@click.option('--config-path', default = 'sie.cfg', help='')
@click.option('--job-id', default = None, help='')
@click.pass_context
@profile
def cli(ctx, config_path, job_id):
    _d('config_path is {0}'.format(config_path))
    _d('job_id is {0}'.format(job_id))
    init_sie_config(config_path)
    if job_id is None and ctx.invoked_subcommand != 'create_job':
        create_id_args = { 'job_id' : job_id }
        job_id = ctx.invoke(create_job, **create_id_args)
        _i('auto created job_id is {0}'.format(job_id))
    if job_id:        
        get_sie_config().set('job', 'job_id', job_id)
    
cli.add_command(to_file_list)
cli.add_command(split_files)
cli.add_command(tfidf_vectorizer)
cli.add_command(normalize_sample)
cli.add_command(sort_tfidf)
cli.add_command(select_k_max)
cli.add_command(build_script_keyword_yar_rule)
cli.add_command(create_job)
cli.add_command(group_sample_2_text)
cli.add_command(group_build_srcipt_keywords_yar)
if __name__ == '__main__':
    cli()