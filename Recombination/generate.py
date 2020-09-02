import Recombination.ctrlGenPar as ctrlGen
import Recombination.runINDELible as runINDELible
import os
import shutil
import multiprocessing as mp
import statistics

import datetime
import Recombination.recombinationPreprocess as recombinationPreprocess
import Recombination.recombinationMerge as recombinationMerge


def run(speciesTree, recombFactor, seqLen, trialIndex, output):
    """
	Worker thread. Runs one trial of ms and INDELible.
	"""

    subFolderName, log = ctrlGen.main(speciesTree, seqLen, recombFactor, trialIndex)
    log = runINDELible.main(subFolderName, log)
    output.put(log)


def main(speciesTree, recombFactor, seqLen, numTrial):
    print(
        "=========================================================================================================================")
    print("[LOG] speciesTree = " + speciesTree + "; recombFactor = " + str(recombFactor) + "; seqLen = " + str(
        seqLen) + "; numTrial = " + str(numTrial))

    folderName = "Recombination/" + speciesTree + "_" + str(seqLen) + "_" + str(recombFactor) + "_" + str(numTrial)
    print("F2:",folderName)
    try:
        os.mkdir(folderName)
    except OSError:
        print("[ERROR] Creation of directory %s failed. Abort process." % folderName)
        return
    else:
        print("[LOG] Successfully created directory: %s" % folderName)

    shutil.copy("Recombination/ms", folderName)
    shutil.copy("Recombination/indelible", folderName)
    os.chdir(folderName)

    # Spawn numTrial processes. Each process runs one trial.
    processes = []
    output = mp.Queue()
    for i in range(numTrial):
        processes.append(mp.Process(target=run, args=(speciesTree, recombFactor, seqLen, i, output)))

    for p in processes:
        p.start()

    for p in processes:
        p.join()

    # Collect log results
    allLogs = [output.get() for p in processes]

    os.chdir("..")
    print("FOLDER: ", folderName)
    return folderName[14:] #required to run recombinationPreprocess

def generate(num_datapoints,tree_label):

    begin_time = datetime.datetime.now()
    num_trials = 6 #dont make bigger than number of cores (parallel processing)
    preprocessDirectory = "Recombination/preprocessedData"
    outputPath = "Recombination/dataClassData"

    iterations = int(num_datapoints / num_trials)

    for i in range(iterations):
        #generate data
        print("generating")
        data_directory = main(speciesTree="HCG", recombFactor=5, seqLen=5, numTrial=num_trials)
        #recombFactor=1, seqLen: 5000000

        #preprocess data
        print("preprocessing")
        print("DATA DIRECTORY", data_directory)
        data_path = f"Recombination/{preprocessDirectory}/recombinant_{i}_"
        recombinationPreprocess.preprocess_data(data_directory, tree_label, data_path)

    #merge preprocessed data
    recombinationMerge.saveData(preprocessDirectory, outputPath)


    print("Total Execution Time: ", datetime.datetime.now() - begin_time)
