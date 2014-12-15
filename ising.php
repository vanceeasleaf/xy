<?php
	for($i=10;$i<=130;$i+=10){
	$fp=fopen("ising_$i.pbs","w");
		fprintf($fp,"
#!/bin/bash -x
#PBS -l nodes=1:ppn=1
#PBS -l walltime=240:00:00
#PBS -j oe
#PBS -q q1.1
#PBS -N ising_$i

#cd $PBS_O_WORKDIR
cd /home/xggong/home1/zhouy/tcscripts/xymodel/
/home/xggong/home1/zhouy/tcscripts/xymodel/ising $i >/home/xggong/home1/zhouy/tcscripts/xymodel/log.ising.$i

exit 0
");
fclose($fp);
	shell_exec("qsub ising_$i.pbs");
	}

	?>
