from modelHandler import TrainAndTest
from models import dnn3,dnn3NoRes
from Recombination.ctrlGenPar import SpeciesTreeInfo
from Recombination.generate import generateAndGet
from ML.IQRAX import runIQTREE, runRAxML, runRAxMLClassification
#Run Sequence Length vs. Accuracy Test
NUM_EPOCHS = 3

#Generate and get data
HCGInfo = SpeciesTreeInfo(name="HCG",mutationRate=2.5e-6, indelRate=0, defaultRecombRate=1.5e-8, popSize=10000, taxaCount=4,
                           postR="-I 4 1 1 1 1 -n 1 1.0 -n 2 1.0 -n 3 1.0 -n 4 1.0 -ej 0.5 1 4 -ej 0.5 2 3 -ej 1.0 4 3")

datasets = generateAndGet(numDatapoints=100,treeLabel=2,sequenceLength=1000,recombFactor=1,speciesTreeInfo=HCGInfo)

print("IQTREE ACCURACY:",runIQTREE(datasets['train']))
