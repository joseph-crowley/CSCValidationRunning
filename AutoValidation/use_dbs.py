from cmseostools import cmsFileManip

def get_files(dataset='', command=''):
    runner = cmsFileManip()
    command = '/cvmfs/cms.cern.ch/common/dasgoclient --limit=0 --query="file,run,lumi,events dataset=' + str(dataset) +  '"'
    result = runner.runCommand(command)
    #print(f'result from runner: \n\n{result}\n\n')
    results = result[0].decode('ascii').split('\n')
    results = [r for r in results if "jsonparser" not in r and "error" not in r]
    r_keys = "file,run,lumi,events,dataset".split(',')
    retval = []
    for r in results[:-1]:
        retval.append(dict(zip(r_keys, r.split(' '))))
    return retval
    


if __name__ == '__main__':
    retval = get_files(dataset = '/Muon/Run2022D-v1/RAW')
    print(retval)

