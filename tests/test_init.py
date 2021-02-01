#!/usr/bin/env python
# basic requirements for test data
import sys
import dandelion as ddl
import pandas as pd
import requests
from io import StringIO

def test_IO():
	file = 'https://cf.10xgenomics.com/samples/cell-vdj/5.0.0/sc5p_v2_hs_B_1k_multi_5gex_b/sc5p_v2_hs_B_1k_multi_5gex_b_vdj_b_airr_rearrangement.tsv'
	r = requests.get(file)
	test_data = pd.read_csv(StringIO(r.text), sep = '\t')
	test_data['locus'] = ['IGH' if 'IGH' in i else 'IGK' if 'IGK' in i else 'IGL' if 'IGL' in i else None for i in test_data.v_call]
	test_data['sample_id'] = '10X'
	test_ddl = ddl.Dandelion(test_data)
	test_ddl.write_h5('test.h5', compression = 'bzip2')
	test_ddl.write_pkl('test.pkl.pbz2')
	test = ddl.read_h5('test.h5')
	_ = ddl.read_pkl('test.pkl.pbz2')
	print(test)

def test_update_metadata():
	test = ddl.read_h5('test.h5')
	ddl.update_metadata(test, 'sequence_id')

def test_find_clones():
	test = ddl.read_h5('test.h5')
	ddl.tl.find_clones()

def test_define_clones():
	test = ddl.read_h5('test.h5')
	ddl.pp.calculate_threshold()
	ddl.tl.define_clones(test, key_added = 'changeo_clone_id')

def test_generate_network():
	test = ddl.read_h5('test.h5')
	ddl.tl.generate_network()

def test_downsampling():
	test = ddl.read_h5('test.h5')
	ddl.tl.generate_network()
	test_downsample = ddl.tl.generate_network(test, downsample = 500)
	print(test_downsample)

def test_quantify_mutation():
	test = ddl.read_h5('test.h5')
	ddl.pp.quantify_mutations()

if __name__ == '__main__':
	test_IO()
	test_update_metadata()
	test_find_clones()
	test_define_clones()
	test_generate_network()
	test_downsampling()
	test_quantify_mutation()

