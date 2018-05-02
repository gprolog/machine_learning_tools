import os, sys
import multiprocessing
import json
from multiprocessing import Manager, Pool, Process
from src.machine_learning.training_process.auto_train_score import *
from src.machine_learning.preprocess.split import *

with open('auto.json', 'r+') as fd:
    cfg = json.load(fd)

middle_dir = cfg['auto_by_engine']['middle_dir']
if cfg['auto_by_engine']['word_freq_function'] == 'TFIDF':
    usetfidf = True
else:
    usetfidf = False

if not os.path.exists(middle_dir):
    os.makedirs(middle_dir)

cur_dir = os.getcwd()
build_dir = os.path.join(cur_dir, 'src', 'tm_pysie', 'build', 'x64')
dllpath = os.path.join(build_dir, 'libtmsie.so')
config_path = os.path.join(cur_dir, 'src', 'pysie', 'pysie.cfg')
auto_cfg_path = os.path.join(cur_dir, 'auto.json')

train_test_mal_sample_path = os.path.join(cfg['auto_by_engine']['train_set_path'], 'mal_set')
train_test_nor_sample_path = os.path.join(cfg['auto_by_engine']['train_set_path'], 'nor_set')

train_out = os.path.join(middle_dir, 'training_feature')
test_out = os.path.join(middle_dir, 'testing_feature')
train_test_out = os.path.join(middle_dir, 'train_test_feature')


train_test_mal_out_file = os.path.join(train_test_out, 'training_test_feature_mal.txt')
train_test_nor_out_file = os.path.join(train_test_out, 'training_test_feature_nor.txt')

train_mal_out_file = os.path.join(train_out, 'training_feature_mal.txt')
train_nor_out_file = os.path.join(train_out, 'training_feature_nor.txt')
test_mal_out_file = os.path.join(test_out, 'testing_feature_mal.txt')
test_nor_out_file = os.path.join(test_out, 'testing_feature_nor.txt')

start_index = cfg['auto_by_engine']['engine_extract_feature_cfg']['start_extract_index']
interval = cfg['auto_by_engine']['engine_extract_feature_cfg']['extract_interval']
topn = cfg['auto_by_engine']['engine_extract_feature_cfg']['use_top_keyword']

if not os.path.exists(train_out):
    os.makedirs(train_out)

if not os.path.exists(test_out):
    os.makedirs(test_out)

if not os.path.exists(train_test_out):
    os.makedirs(train_test_out)


def run_cmd(cmd):
    print cmd
    os.system(cmd)

for start_index in range(start_index, topn+interval, interval):
    os.chdir(build_dir)
    if True:
	if cfg['auto_by_engine']['enable_extract_feature']:
	    cmd_list = []
	    proc_pool = Pool(multiprocessing.cpu_count())
	    cmd_list.append('python ../../py_talos.py --usetfidf={} --dllpath={} --samplepath={} --label={} --topn={} --out={} --configpath={} --start_extract_index={} --interval={}'.format(usetfidf, dllpath, train_test_mal_sample_path,1,topn,train_test_mal_out_file, config_path, start_index, interval))
	    cmd_list.append('python ../../py_talos.py --usetfidf={} --dllpath={} --samplepath={} --label={} --topn={} --out={} --configpath={} --start_extract_index={} --interval={}'.format(usetfidf, dllpath, train_test_nor_sample_path,0,topn,train_test_nor_out_file, config_path, start_index, interval))

	    for cmd in cmd_list:
		proc_pool.apply_async(run_cmd, args=(cmd,))
	    proc_pool.close()
	    proc_pool.join()

	# split feature files
	working_dir = os.path.join(cur_dir,'src', 'machine_learning', 'preprocess')
	os.chdir(working_dir)

	dest_file_dir = os.path.join(middle_dir, 'feature_set_' + str(start_index))
	if not os.path.exists(dest_file_dir):
	    os.makedirs(dest_file_dir)
		
	for f in os.listdir(train_test_out):
	    print f
	    if f.startswith('training_test_feature_'):
		cur_file_path = os.path.join(train_test_out, f)
		cmd = 'mv ' + cur_file_path + ' ' + dest_file_dir
		print cmd
		os.system(cmd)

	if True:
	    cmd = 'cat '+ dest_file_dir + '/training_test_feature_mal.txt_* > ' + dest_file_dir + '/training_test_mal.txt'
	    print cmd
	    os.system(cmd)
	    cmd = 'cat '+ dest_file_dir + '/training_test_feature_nor.txt_* > ' + dest_file_dir + '/training_test_nor.txt'
	    print cmd
	    os.system(cmd)
	    cmd = 'python split.py ' + os.path.join(dest_file_dir, 'training_test_nor.txt')  + ' ' + '0.7'
	    print cmd
	    os.system(cmd)    
	    cmd = 'python split.py ' + os.path.join(dest_file_dir, 'training_test_mal.txt')  + ' ' + '0.7'
	    print cmd
	    os.system(cmd)    
	    
	    group_a = []
	    group_b = []
	    for f in os.listdir(dest_file_dir):
		if f.find('group_a') != -1:
		    group_a.append(f)
		if f.find('group_b') != -1:
		    group_b.append(f)
	    tempcmd = ''
	    for item in group_a:
		tempcmd += os.path.join(dest_file_dir, item) + ' '
	    target_train_file = os.path.join(dest_file_dir, 'training.feature')
	    if os.path.exists(target_train_file):
		os.system('rm -f ' + target_train_file)
	    cmd = 'cat ' + tempcmd + '> ' + target_train_file
	    print cmd
	    os.system(cmd)
	    tempcmd = ''
	    for item in group_b:
		tempcmd += os.path.join(dest_file_dir, item) + ' '
	    target_test_file = os.path.join(dest_file_dir, 'testing.feature')
	    if os.path.exists(target_test_file):
		os.system('rm -f ' + target_test_file)
	    cmd = 'cat ' + tempcmd + '> ' + target_test_file
	    print cmd
	    os.system(cmd)
		    

	# training and test the model
	train_dir = os.path.join(cur_dir, 'src', 'machine_learning', 'training_process')
	os.chdir(train_dir)


	def run_task(middle, training_path, testing_path):
	    cmd = 'python auto_train_score.py {} {} {}'.format(middle, training_path, testing_path)
	    print cmd
	    os.system(cmd)


	proc_pool = Pool(multiprocessing.cpu_count())
	training_file_path = os.path.join(dest_file_dir, 'training.feature')
	testing_file_path = os.path.join(dest_file_dir, 'testing.feature')
	proc_pool.apply_async(run_task, args=(dest_file_dir, training_file_path, testing_file_path))

	proc_pool.close()
	proc_pool.join()
	print 'training and predict model done!'
    os.chdir(cur_dir)
