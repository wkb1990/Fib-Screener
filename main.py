import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime

today = datetime.today()
formatted_date = today.strftime('%d%m%y')

sd = "2022-01-01"
ed = "2024-03-28"

#calculate RSI levels
def calculate_rsi(data, window):
    delta = data.diff()
    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0

    average_gain = up.rolling(window).mean()
    average_loss = abs(down.rolling(window).mean())

    rs = average_gain / average_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

ticker = ["14D.AX","29M.AX","T3D.AX","TGP.AX","TCF.AX","TOT.AX","TDO.AX","3PL.AX","4DX.AX","4DS.AX","5EA.AX","88E.AX","8CO.AX","8IH.AX","8VI.AX","92E.AX","AYI.AX","A2B.AX","ABG.AX","ASK.AX","ABX.AX","AKG.AX","AX8.AX","AX1.AX","ACS.AX","ADC.AX","ACQ.AX","ACF.AX","ACR.AX","ACW.AX","ATV.AX","AIV.AX","ACU.AX","ACE.AX","AD1.AX","ADA.AX","ADH.AX","1AD.AX","ADD.AX","ABC.AX","ADG.AX","ADR.AX","AI1.AX","ADY.AX","ABY.AX","AHL.AX","ADT.AX","ADS.AX","AVM.AX","ANO.AX","ABV.AX","AHI.AX","AV1.AX","ADX.AX","AER.AX","AML.AX","AEI.AX","AIS.AX","AMX.AX","AFL.AX","AF1.AX","AF2.AX","AF3.AX","A1G.AX","AFP.AX","AGL.AX","AMN.AX","AGR.AX","AIM.AX","A1M.AX","APW.AX","AGI.AX","AIZ.AX","ART.AX","AJL.AX","AKO.AX","AUQ.AX","ALB.AX","ALY.AX","ALC.AX","AL8.AX","ARN.AX","AJX.AX","1AI.AX","AQI.AX","AQX.AX","ALK.AX","AMT.AX","AQZ.AX","AXN.AX","AGE.AX","AKE.AX","APS.AX","ALM.AX","AII.AX","A4N.AX","ALQ.AX","AZI.AX","ATC.AX","ATH.AX","AIQ.AX","1AG.AX","AGH.AX","ALU.AX","AME.AX","AWC.AX","ALV.AX","AMA.AX","3DA.AX","ANL.AX","AMO.AX","AMH.AX","AMC.AX","ARR.AX","AW1.AX","AL3.AX","AMP.AX","ATX.AX","ALD.AX","AN1.AX","ANR.AX","ANX.AX","ADN.AX","ATM.AX","AND.AX","ANN.AX","ASN.AX","ADO.AX","AVR.AX","AAU.AX","AZY.AX","ANP.AX","ANZ.AX","APA.AX","AP2.AX","AHX.AX","APM.AX","AON.AX","AOL.AX","AO2.AX","AO3.AX","APX.AX","AFW.AX","AQN.AX","ARU.AX","ARB.AX","ARC.AX","AM7.AX","LTM.AX","AXE.AX","AR9.AX","ARL.AX","ADV.AX","ARF.AX","AGN.AX","ARD.AX","ALI.AX","ARG.AX","ARE.AX","AGY.AX","ARA.AX","ALL.AX","AZL.AX","AHK.AX","AMM.AX","AJQ.AX","A1N.AX","ARX.AX","ALA.AX","AMD.AX","ARV.AX","ATG.AX","AYA.AX","AAJ.AX","AJY.AX","AS1.AX","AFA.AX","AMG.AX","ASH.AX","ATB.AX","AS2.AX","APZ.AX","ASP.AX","AKM.AX","ASR.AX","ASV.AX","AO1.AX","APL.AX","ASO.AX","AAR.AX","ATR.AX","ASE.AX","ASX.AX","AHN.AX","A11.AX","ALX.AX","ATP.AX","AT1.AX","AMS.AX","ATU.AX","ATA.AX","AUB.AX","AIA.AX","AVC.AX","ACP.AX","AUA.AX","AD8.AX","AKP.AX","AUG.AX","AKN.AX","AUK.AX","AEE.AX","AMI.AX","AWJ.AX","AUR.AX","AZJ.AX","1AE.AX","A3D.AX","AUE.AX","AUN.AX","AC8.AX","AUC.AX","AOA.AX","ANV.AX","AQD.AX","ABB.AX","ASB.AX","AUH.AX","AHC.AX","ANG.AX","AYT.AX","AGD.AX","AR1.AX","A8G.AX","AN3.AX","AYM.AX","AAC.AX","AAP.AX","ABE.AX","ACL.AX","XCL.AX","ACM.AX","AHF.AX","AEF.AX","AFG.AX","AFI.AX","AGC.AX","AUZ.AX","AQC.AX","APC.AX","AR3.AX","ASQ.AX","ASM.AX","AUI.AX","AYU.AX","AOF.AX","AVL.AX","AVG.AX","ATS.AX","ABA.AX","ASG.AX","AVA.AX","AVD.AX","AVE.AX","AEV.AX","AVW.AX","AVH.AX","AVJ.AX","AVZ.AX","AXI.AX","AXP.AX","AZS.AX","BBN.AX","BPP.AX","BTI.AX","BMM.AX","BMR.AX","B01.AX","BOQ.AX","BMN.AX","BAP.AX","BGD.AX","BSE.AX","BSN.AX","BAS.AX","BMO.AX","BRL.AX","BM8.AX","BAT.AX","BMH.AX","BDX.AX","BCI.AX","BPT.AX","BLX.AX","BCN.AX","BCC.AX","BMT.AX","B4P.AX","BGA.AX","BRX.AX","BFG.AX","BVR.AX","BGL.AX","BEN.AX","BHD.AX","BEL.AX","BNZ.AX","BEO.AX","BKY.AX","BEZ.AX","BFC.AX","BET.AX","BHP.AX","BRI.AX","BTH.AX","BEX.AX","BIM.AX","BGT.AX","BIO.AX","BIT.AX","BXN.AX","BDT.AX","BIS.AX","BKI.AX","BCA.AX","BC8.AX","BDG.AX","BME.AX","BKT.AX","BSX.AX","BWF.AX","BLZ.AX","SQ2.AX","BLU.AX","BNL.AX","BBT.AX","BCT.AX","BSL.AX","BLG.AX","BMG.AX","BBC.AX","BML.AX","BOA.AX","BLY.AX","BOD.AX","BKG.AX","BOL.AX","BLD.AX","BOE.AX","BTE.AX","BOT.AX","BOC.AX","BUY.AX","BCB.AX","BPH.AX","BP8.AX","BPM.AX","BRN.AX","BXB.AX","BVS.AX","BCM.AX","BRE.AX","BRG.AX","BKW.AX","BGE.AX","BTR.AX","BBL.AX","BGP.AX","BCK.AX","BEE.AX","BRK.AX","BYH.AX","BSA.AX","BFL.AX","BTC.AX","BUS.AX","BUB.AX","BNR.AX","BDM.AX","BUR.AX","BRU.AX","BTN.AX","BUX.AX","BWP.AX","BWX.AX","BYE.AX","C29.AX","CDM.AX","CDO.AX","CCM.AX","DXA.AX","CAI.AX","CE1.AX","CXL.AX","CHL.AX","CLB.AX","CGB.AX","CAN.AX","CAE.AX","CBY.AX","CAY.AX","CAG.AX","CAJ.AX","CAA.AX","CRS.AX","CMM.AX","CAQ.AX","CAR.AX","CVV.AX","CWX.AX","CRB.AX","CRM.AX","CG1.AX","CDX.AX","CDD.AX","CTQ.AX","CDP.AX","CIN.AX","CL8.AX","CNB.AX","CVN.AX","CAV.AX","CCE.AX","CCV.AX","CPN.AX","CMD.AX","CST.AX","CCZ.AX","CDT.AX","CSF.AX","CTN.AX","CYL.AX","CAT.AX","CXU.AX","CVR.AX","CAZ.AX","CD1.AX","CD2.AX","CD3.AX","CWP.AX","CLA.AX","CTM.AX","CTP.AX","CAF.AX","CXM.AX","CNI.AX","C2F.AX","CIP.AX","COF.AX","CTT.AX","CFO.AX","CGR.AX","CHN.AX","CEL.AX","CGF.AX","CHJ.AX","CIA.AX","CCA.AX","CHR.AX","CC9.AX","CHC.AX","CLW.AX","CQR.AX","CQE.AX","CMX.AX","CHW.AX","CHM.AX","CNU.AX","C79.AX","CTO.AX","CCX.AX","CVL.AX","C7A.AX","CU6.AX","CLZ.AX","CSS.AX","CNQ.AX","CWY.AX","CSX.AX","CVW.AX","CPV.AX","COV.AX","CAM.AX","CIW.AX","CUV.AX","CLG.AX","CLV.AX","CLU.AX","CEH.AX","COB.AX","CBO.AX","CBE.AX","COH.AX","COD.AX","CDA.AX","CDR.AX","COG.AX","CGS.AX","CHK.AX","CKA.AX","COL.AX","CKF.AX","CRL.AX","COI.AX","CBA.AX","CCG.AX","CF1.AX","CMP.AX","CPU.AX","CNJ.AX","CIO.AX","CXZ.AX","CRD.AX","CR1.AX","CT1.AX","CEN.AX","CBL.AX","CBH.AX","COE.AX","CPM.AX","CUS.AX","CSE.AX","COY.AX","CZN.AX","CXO.AX","CR9.AX","CRN.AX","CTD.AX","CMO.AX","C1X.AX","COS.AX","CGC.AX","CUP.AX","CYG.AX","CGO.AX","CXX.AX","CCR.AX","CCP.AX","CI1.AX","CMG.AX","CRR.AX","CMW.AX","CTE.AX","CPL.AX","CSL.AX","CSR.AX","CLX.AX","CUE.AX","CUF.AX","CUL.AX","CPO.AX","CVB.AX","CVC.AX","CYQ.AX","CLE.AX","CYC.AX","CY5.AX","CYP.AX","CYM.AX","CZR.AX","DAL.AX","DBI.AX","DTC.AX","DNK.AX","DTM.AX","DTL.AX","DDT.AX","DTR.AX","DEG.AX","DEM.AX","DCG.AX","DYL.AX","DEL.AX","DLI.AX","DGH.AX","DM1.AX","DMC.AX","DES.AX","DRR.AX","DVP.AX","DEV.AX","DXS.AX","DXC.AX","DXI.AX","DGL.AX","DGR.AX","DBO.AX","DRX.AX","DDR.AX","DCC.AX","DXB.AX","DAF.AX","DCX.AX","DVR.AX","DUI.AX","DJW.AX","DMM.AX","DOC.AX","DCL.AX","DHG.AX","DME.AX","DLM.AX","DMP.AX","DNA.AX","DOR.AX","DVL.AX","DTZ.AX","DOU.AX","DOW.AX","DRA.AX","DMG.AX","DRF.AX","DRE.AX","DAM.AX","DAT.AX","DRO.AX","DSE.AX","DTI.AX","DUB.AX","DUG.AX","DKM.AX","DUN.AX","DUR.AX","DSK.AX","DBF.AX","D2O.AX","DXN.AX","DY6.AX","DDB.AX","DYM.AX","EP1.AX","E79.AX","APE.AX","EM2.AX","EPY.AX","E33.AX","EMS.AX","EFE.AX","EBO.AX","EBR.AX","ECG.AX","EIQ.AX","EPM.AX","EOF.AX","EGR.AX","ECP.AX","ECS.AX","EDE.AX","EDU.AX","EDC.AX","ECF.AX","ENN.AX","ELD.AX","EOS.AX","E25.AX","ELT.AX","EL8.AX","EXL.AX","EXR.AX","ELE.AX","ELS.AX","EVO.AX","EMB.AX","EHL.AX","EMR.AX","EMT.AX","EMI.AX","EML.AX","ERM.AX","EMP.AX","EEG.AX","ERL.AX","EMU.AX","EMV.AX","EMD.AX","ENR.AX","EDV.AX","ERG.AX","ENX.AX","EAX.AX","EME.AX","EOL.AX","ERA.AX","EGY.AX","ETM.AX","EWC.AX","EGG.AX","EGN.AX","ENL.AX","ENV.AX","EEL.AX","ENT.AX","ETR.AX","ECT.AX","EGL.AX","EVS.AX","EPX.AX","EPN.AX","EQR.AX","EQT.AX","EQX.AX","EQN.AX","EQS.AX","EQE.AX","ERD.AX","ERW.AX","ESR.AX","ESK.AX","EBG.AX","EGH.AX","EMN.AX","EUR.AX","EMH.AX","EZL.AX","EVR.AX","EVE.AX","EMC.AX","EG1.AX","EVG.AX","EV1.AX","EVN.AX","EVT.AX","EVZ.AX","ECL.AX","EXT.AX","EX1.AX","EXP.AX","EZZ.AX","FAL.AX","FEG.AX","FAR.AX","FNR.AX","FRM.AX","FPC.AX","FPP.AX","FFG.AX","FBR.AX","FXG.AX","FLX.AX","FEX.AX","FTZ.AX","FFI.AX","FID.AX","FSG.AX","FIN.AX","FRI.AX","FDR.AX","FND.AX","FCL.AX","FNX.AX","FTC.AX","FRB.AX","FRE.AX","FFX.AX","FFM.AX","FTL.AX","FA2.AX","FAU.AX","FGR.AX","FL1.AX","FM3.AX","FM2.AX","FM5.AX","FM4.AX","FM1.AX","FCT.AX","FPH.AX","FZR.AX","FSI.AX","FPR.AX","FWD.AX","FBU.AX","FA1.AX","FRX.AX","FLT.AX","FLC.AX","FG1.AX","FML.AX","FSF.AX","FOR.AX","FFF.AX","FGH.AX","FRS.AX","FMG.AX","FOS.AX","FCG.AX","FHS.AX","FLN.AX","FRW.AX","FDV.AX","FHE.AX","FGL.AX","FSA.AX","FSE.AX","FBM.AX","FGX.AX","FGG.AX","FME.AX","GUD.AX","G11.AX","GEM.AX","GLN.AX","GAP.AX","G1A.AX","GLL.AX","GAL.AX","GDF.AX","GGX.AX","GML.AX","GTH.AX","GBZ.AX","GCX.AX","GDI.AX","GDG.AX","GNE.AX","GMD.AX","GES.AX","GSS.AX","GTG.AX","GNX.AX","GEN.AX","GTK.AX","GNP.AX","GPR.AX","GIB.AX","GLA.AX","GC1.AX","GLE.AX","GDC.AX","GLH.AX","GL1.AX","GFL.AX","GLV.AX","GUE.AX","GLB.AX","GBE.AX","GRL.AX","G50.AX","GHY.AX","GMN.AX","GOR.AX","GCR.AX","GED.AX","GGR.AX","G88.AX","GSM.AX","GDA.AX","GMG.AX","GOW.AX","GPT.AX","GQG.AX","GNG.AX","GNC.AX","GGE.AX","GRR.AX","GTI.AX","GBR.AX","GR8.AX","GDM.AX","GNM.AX","GSN.AX","GTE.AX","GCM.AX","GT1.AX","H2G.AX","GSR.AX","GRE.AX","GRV.AX","GW1.AX","GRX.AX","G6M.AX","GOZ.AX","GCI.AX","GTR.AX","GTN.AX","GUL.AX","GWA.AX","GWR.AX","HCF.AX","HLF.AX","HAL.AX","HMG.AX","HMX.AX","HNG.AX","HSN.AX","HAR.AX","HMY.AX","HT8.AX","HHR.AX","HTG.AX","HVN.AX","HAS.AX","HAV.AX","HIO.AX","HAW.AX","HZR.AX","HLS.AX","HPP.AX","HCW.AX","HGH.AX","HM1.AX","HVY.AX","HRE.AX","HLI.AX","HE8.AX","HLX.AX","HLO.AX","HMD.AX","HXG.AX","HXL.AX","HPR.AX","HTM.AX","HCL.AX","HFR.AX","HGO.AX","HPG.AX","HMI.AX","HIT.AX","HIQ.AX","HMC.AX","HCT.AX","HDN.AX","HRN.AX","HRZ.AX","HZN.AX","HOR.AX","HCH.AX","HPI.AX","HAU.AX","HUB.AX","HFY.AX","HGL.AX","HUM.AX","HTA.AX","HYD.AX","HCD.AX","HGV.AX","HYT.AX","HCS.AX","IS3.AX","ICI.AX","ICL.AX","ICE.AX","ICN.AX","ID8.AX","IEL.AX","IDT.AX","IGN.AX","IGO.AX","IKE.AX","ILT.AX","ILU.AX","IMA.AX","IBX.AX","IMD.AX","IME.AX","IMC.AX","IMM.AX","IPT.AX","IPD.AX","IPC.AX","IMR.AX","IMU.AX","ICG.AX","INP.AX","IPL.AX","IAM.AX","IDA.AX","IND.AX","I88.AX","INF.AX","IMI.AX","IFM.AX","IFT.AX","INA.AX","ING.AX","IRX.AX","INL.AX","IIQ.AX","IFL.AX","IAG.AX","IDX.AX","IRI.AX","ICR.AX","IMB.AX","IEQ.AX","IFX.AX","IG6.AX","IMG.AX","IMX.AX","IMQ.AX","IMO.AX","IEC.AX","IVT.AX","IVR.AX","ICU.AX","INV.AX","IXC.AX","IVZ.AX","IVX.AX","IOD.AX","ION.AX","INR.AX","IXR.AX","IOU.AX","IPB.AX","IPG.AX","IPX.AX","IPH.AX","IRE.AX","IR1.AX","IRD.AX","IBC.AX","IBG.AX","ILA.AX","ITM.AX","IGL.AX","IXU.AX","JGH.AX","JBY.AX","JHX.AX","JAL.AX","JAN.AX","JAT.AX","JAV.AX","JTL.AX","JAY.AX","JBH.AX","JCS.AX","JRV.AX","JLL.AX","JLG.AX","JYC.AX","JDO.AX","JIN.AX","JNO.AX","JPR.AX","JMS.AX","KSC.AX","KTG.AX","KAM.AX","K2F.AX","KDY.AX","KLR.AX","KAI.AX","KAU.AX","KZR.AX","KAL.AX","KM1.AX","KPO.AX","KLL.AX","KAR.AX","KAT.AX","KPG.AX","KLS.AX","KEY.AX","KBC.AX","KED.AX","KFW.AX","KGL.AX","KLI.AX","KIN.AX","KSL.AX","KYP.AX","KCC.AX","KKO.AX","KRR.AX","KFM.AX","KIG.AX","KI1.AX","KCN.AX","KNG.AX","KRM.AX","KSN.AX","KME.AX","KKC.AX","KMD.AX","KNM.AX","KNO.AX","KOB.AX","KGN.AX","KNB.AX","KOR.AX","KP2.AX","KOV.AX","KTA.AX","KGD.AX","KNI.AX","LSF.AX","LTF.AX","LT1.AX","LT3.AX","LT4.AX","LT5.AX","LT6.AX","LT2.AX","LT7.AX","LT8.AX","LRL.AX","LSA.AX","LKE.AX","LKO.AX","LHM.AX","LNR.AX","LAM.AX","LRK.AX","LRV.AX","LBL.AX","LRS.AX","LCN.AX","LC1.AX","LC2.AX","LFS.AX","LMG.AX","LAW.AX","LBT.AX","LCL.AX","LM1.AX","LEX.AX","LCY.AX","LGM.AX","LEG.AX","LLC.AX","LLL.AX","LPD.AX","LGI.AX","LIS.AX","LFG.AX","LI2.AX","LI5.AX","LI6.AX","LP1.AX","LI7.AX","LI9.AX","360.AX","LIC.AX","LNW.AX","L1M.AX","LML.AX","LIN.AX","LAU.AX","LNU.AX","LNK.AX","LIO.AX","LLO.AX","LSX.AX","LI8.AX","LN1.AX","LTR.AX","LIT.AX","LEL.AX","LPM.AX","LPI.AX","LU7.AX","LGP.AX","LV1.AX","LVH.AX","LVT.AX","LO1.AX","LPE.AX","LKY.AX","LDR.AX","LSR.AX","LCE.AX","LRD.AX","LOT.AX","LVE.AX","LOV.AX","LRT.AX","LLI.AX","LTP.AX","LOM.AX","LDX.AX","LM8.AX","LYN.AX","LYL.AX","LYK.AX","LYC.AX","LGL.AX","M3M.AX","M8S.AX","MAF.AX","MGH.AX","MIO.AX","M7T.AX","MAH.AX","MBL.AX","MQG.AX","MAQ.AX","M4M.AX","MPA.AX","MAD.AX","MFG.AX","MGF.AX","MBH.AX","MAG.AX","MAU.AX","MGT.AX","MNS.AX","MGU.AX","MGL.AX","MKG.AX","M24.AX","MAN.AX","MHC.AX","MTL.AX","MKR.AX","MPK.AX","MCX.AX","MMM.AX","MEU.AX","MMA.AX","MQR.AX","MVL.AX","MZZ.AX","MCE.AX","MAT.AX","MXR.AX","MXI.AX","MFD.AX","MYG.AX","MYX.AX","MRL.AX","MCM.AX","MEA.AX","MMS.AX","MCP.AX","MSG.AX","MMR.AX","MDR.AX","MM8.AX","MPZ.AX","MZF.AX","MZT.AX","MZ1.AX","MZ2.AX","MPL.AX","MVP.AX","MDC.AX","MEK.AX","MEG.AX","MP1.AX","MAY.AX","ME1.AX","MEM.AX","MHI.AX","MCY.AX","MEZ.AX","MSB.AX","MBK.AX","MHK.AX","MCT.AX","MLM.AX","MLS.AX","MLX.AX","MGA.AX","MTC.AX","MYE.AX","MTS.AX","MEI.AX","MEL.AX","MOT.AX","MXT.AX","MF1.AX","MF2.AX","MF3.AX","MMI.AX","MPP.AX","MFF.AX","MXC.AX","MHJ.AX","MX1.AX","MAP.AX","MAM.AX","MM1.AX","MDI.AX","MWY.AX","MWL.AX","MCL.AX","MKL.AX","MIL.AX","MNB.AX","MDX.AX","MRC.AX","MIN.AX","MI6.AX","MG1.AX","MRR.AX","M2R.AX","MIR.AX","MGR.AX","MSV.AX","MTH.AX","MMC.AX","MLG.AX","MRM.AX","MOM.AX","MOH.AX","MND.AX","MVF.AX","MME.AX","MRZ.AX","1MC.AX","MEC.AX","MOZ.AX","MXO.AX","MTO.AX","MTB.AX","MGX.AX","MRD.AX","MOV.AX","MPR.AX","MRQ.AX","M2M.AX","MTM.AX","MSI.AX","MCA.AX","MPX.AX","MBX.AX","MRI.AX","MYR.AX","MYS.AX","N1H.AX","NAG.AX","NAM.AX","NC6.AX","NAN.AX","NVU.AX","NCC.AX","NAC.AX","NSC.AX","NYM.AX","NAB.AX","NAJ.AX","NRM.AX","NRO.AX","NRP.AX","NSR.AX","NTD.AX","NBS.AX","NMR.AX","NML.AX","NGI.AX","NBI.AX","NES.AX","NMT.AX","NET.AX","NWL.AX","NEU.AX","NRZ.AX","NSB.AX","NTI.AX","NAE.AX","NHC.AX","XNC.AX","NTL.AX","NWC.AX","NZS.AX","NZK.AX","NZO.AX","NWF.AX","NPR.AX","NEM.AX","NPM.AX","NWS.AX","NME.AX","NXG.AX","NNG.AX","NXS.AX","NXT.AX","NXD.AX","NXM.AX","NGE.AX","NGX.AX","NHF.AX","NCK.AX","NIC.AX","NIS.AX","NKL.AX","NC1.AX","NDO.AX","NGL.AX","NIM.AX","NEC.AX","NHE.AX","NOL.AX","NIB.AX","NNL.AX","NFL.AX","NRX.AX","NSM.AX","NTU.AX","NST.AX","NWM.AX","NOR.AX","NOU.AX","EYE.AX","NVA.AX","NOV.AX","NVQ.AX","NVO.AX","NVX.AX","NOX.AX","NWH.AX","NSX.AX","NTM.AX","NUC.AX","NCR.AX","NGY.AX","NFN.AX","NUF.AX","NUH.AX","NXL.AX","NGS.AX","NYR.AX","NZM.AX","OKJ.AX","OAK.AX","OAR.AX","OCL.AX","OCN.AX","OCA.AX","OCT.AX","OD6.AX","ODE.AX","ODY.AX","OFX.AX","OLH.AX","OLI.AX","OLY.AX","OMH.AX","OMA.AX","OBL.AX","OM1.AX","OSL.AX","1CG.AX","ONE.AX","OML.AX","OLL.AX","OPN.AX","OPH.AX","OPT.AX","OIL.AX","OPL.AX","OBM.AX","OAU.AX","OMX.AX","OEC.AX","ODA.AX","ZOR.AX","ORR.AX","OXT.AX","ORI.AX","ORG.AX","OEQ.AX","ORM.AX","ORN.AX","ORA.AX","OCC.AX","OSM.AX","OSX.AX","OEL.AX","OZM.AX","OZZ.AX","PGO.AX","PAC.AX","PEB.AX","PNM.AX","PSQ.AX","PGH.AX","PCK.AX","PDN.AX","PAM.AX","PCL.AX","PAN.AX","PFE.AX","PNT.AX","PNR.AX","PPY.AX","PBL.AX","PAR.AX","PGC.AX","PKD.AX","PWN.AX","PL3.AX","PSL.AX","PMT.AX","PAT.AX","PAB.AX","PUA.AX","PEK.AX","PKO.AX","PLG.AX","PEX.AX","PPC.AX","PCG.AX","PIA.AX","PE1.AX","PEN.AX","5GG.AX","PPE.AX","PPM.AX","PP1.AX","PU1.AX","PEA.AX","PEV.AX","PE4.AX","PE5.AX","PU6.AX","PIL.AX","PGD.AX","PRN.AX","PCI.AX","PIC.AX","PPT.AX","PEC.AX","PRU.AX","PWR.AX","PTR.AX","PXA.AX","PAA.AX","PHX.AX","PHO.AX","PET.AX","PLL.AX","PLS.AX","PGY.AX","PNI.AX","PIM.AX","PNC.AX","PLN.AX","PVT.AX","PGM.AX","PAI.AX","PTM.AX","PMC.AX","PL8.AX","PLY.AX","PLT.AX","PGF.AX","PNX.AX","PVE.AX","POD.AX","3DP.AX","PBH.AX","PXX.AX","POL.AX","PNV.AX","POS.AX","PNN.AX","PVL.AX","PPK.AX","PPS.AX","PDI.AX","PMV.AX","PTX.AX","PTL.AX","PFG.AX","PRG.AX","PME.AX","PPG.AX","PBP.AX","PRX.AX","POT.AX","POV.AX","POX.AX","POA.AX","POB.AX","POC.AX","POF.AX","POE.AX","PRM.AX","PFP.AX","PHL.AX","PRO.AX","PGL.AX","PRS.AX","PSC.AX","POW.AX","PIQ.AX","PV1.AX","PRL.AX","PRT.AX","PSI.AX","PUQ.AX","PU2.AX","PFT.AX","PH2.AX","PR1.AX","PPL.AX","PO3.AX","PUR.AX","PVW.AX","PWH.AX","PYC.AX","QAN.AX","QIP.AX","QBE.AX","QEM.AX","QML.AX","QNB.AX","QOR.AX","QAL.AX","QRI.AX","QGL.AX","QUB.AX","QPM.AX","XQL.AX","QUE.AX","QFE.AX","QHL.AX","QVE.AX","QXR.AX","R3D.AX","RAC.AX","RAD.AX","RAG.AX","RAS.AX","RDN.AX","RZI.AX","REP.AX","RMS.AX","RHC.AX","RND.AX","RAN.AX","RPG.AX","RFA.AX","REE.AX","RTH.AX","RBR.AX","REA.AX","RR1.AX","RCL.AX","RDY.AX","RCE.AX","REC.AX","RKN.AX","RFT.AX","RED.AX","RHK.AX","RHI.AX","RDM.AX","RMX.AX","ROG.AX","RC1.AX","RFX.AX","RIL.AX","RDX.AX","RDS.AX","REH.AX","RLC.AX","RCT.AX","RG8.AX","RF1.AX","RPL.AX","R8R.AX","RGS.AX","RGN.AX","REX.AX","REG.AX","RRL.AX","RWC.AX","REM.AX","RNU.AX","RNX.AX","RLT.AX","RNT.AX","RNE.AX","RMC.AX","RA2.AX","RMD.AX","RSG.AX","RML.AX","RHT.AX","RBX.AX","RDG.AX","RMI.AX","REZ.AX","RSH.AX","RBD.AX","RFG.AX","RVS.AX","RRR.AX","RWD.AX","RXH.AX","RXM.AX","REY.AX","RNO.AX","RHY.AX","SGL.AX","RVT.AX","RIC.AX","RIE.AX","RIM.AX","RCR.AX","RIO.AX","RGL.AX","RLF.AX","RMY.AX","ROC.AX","RKT.AX","RON.AX","RLG.AX","ROO.AX","RGI.AX","RXL.AX","RPM.AX","RUL.AX","RTG.AX","RWL.AX","RB6.AX","RB1.AX","RTR.AX","RFF.AX","RYD.AX","S2R.AX","SBR.AX","SGC.AX","SRH.AX","SAN.AX","SB2.AX","SFR.AX","SNC.AX","SFM.AX","SMI.AX","SFV.AX","STO.AX","SRR.AX","SGA.AX","STN.AX","SND.AX","SVG.AX","SYA.AX","SCG.AX","SCW.AX","SCA.AX","SFC.AX","SCL.AX","SDV.AX","SCN.AX","SCT.AX","SDI.AX","SFG.AX","SES.AX","SEK.AX","SHV.AX","SWF.AX","SEN.AX","SNS.AX","S3N.AX","SEQ.AX","WSZ.AX","WEK.AX","WEJ.AX","RFC.AX","BA2.AX","WE1.AX","WB1.AX","WSE.AX","SKO.AX","SRV.AX","SSM.AX","SVW.AX","SWM.AX","SZL.AX","SGF.AX","SHA.AX","SSG.AX","SFX.AX","SBW.AX","SHJ.AX","SHZ.AX","SHM.AX","SI6.AX","SNX.AX","SRX.AX","SSL.AX","SIG.AX","SIH.AX","SLX.AX","SLH.AX","SLR.AX","SVL.AX","SIS.AX","SIO.AX","SGM.AX","SHG.AX","SRI.AX","SNG.AX","SIT.AX","SDR.AX","SIV.AX","SKN.AX","SKS.AX","SKY.AX","SKT.AX","SKC.AX","SPZ.AX","SIQ.AX","SMP.AX","SOC.AX","SLM.AX","SLS.AX","SVR.AX","SOM.AX","SHL.AX","SHP.AX","S32.AX","SXE.AX","SXG.AX","SXL.AX","SUH.AX","SPD.AX","SOV.AX","SVM.AX","SPA.AX","SPN.AX","SPK.AX","SPR.AX","STW.AX","SLF.AX","SFY.AX","SP3.AX","SPX.AX","SEC.AX","ST1.AX","SEG.AX","SHO.AX","SIX.AX","SQX.AX","SRG.AX","SRJ.AX","SSH.AX","SSR.AX","SBM.AX","SGQ.AX","SCD.AX","SMR.AX","S66.AX","SMS.AX","SPL.AX","GAS.AX","GVF.AX","SVY.AX","SDF.AX","SGI.AX","SST.AX","SLB.AX","SRZ.AX","STP.AX","SGP.AX","SHE.AX","SRY.AX","STG.AX","STA.AX","SRT.AX","SOR.AX","SER.AX","SP8.AX","STK.AX","STX.AX","SRK.AX","SMN.AX","SLZ.AX","SNZ.AX","SUM.AX","SUN.AX","SRL.AX","SHN.AX","STM.AX","SUL.AX","SPQ.AX","SLC.AX","SNL.AX","SRN.AX","SUV.AX","SW1.AX","SWP.AX","SYM.AX","SOP.AX","SM1.AX","SNT.AX","SYR.AX","TAH.AX","T88.AX","TLG.AX","TD1.AX","TLM.AX","TAL.AX","TWD.AX","TBN.AX","TMB.AX","TAM.AX","TAR.AX","TFL.AX","TSK.AX","TAS.AX","TIP.AX","TG1.AX","TMT.AX","TNE.AX","TLX.AX","TL1.AX","TLS.AX","TEM.AX","TPW.AX","TMR.AX","X64.AX","TMS.AX","T92.AX","TER.AX","TGH.AX","TMX.AX","TZN.AX","TSO.AX","TES.AX","TG6.AX","A2M.AX","AU1.AX","WAG.AX","CCO.AX","GO2.AX","HPC.AX","TLC.AX","MKT.AX","OJC.AX","TRS.AX","SGR.AX","TGM.AX","TMZ.AX","THR.AX","TOP.AX","TEK.AX","1TT.AX","TIA.AX","TIE.AX","TIG.AX","TML.AX","TNY.AX","TRP.AX","TTM.AX","TSL.AX","TTT.AX","TVN.AX","TOU.AX","TMK.AX","TOK.AX","TI1.AX","TBA.AX","TEE.AX","TSI.AX","TOE.AX","TOR.AX","TOZ.AX","TNJ.AX","TTZ.AX","TRE.AX","TVL.AX","THL.AX","TWR.AX","TOY.AX","TPC.AX","TPG.AX","TTI.AX","TRJ.AX","TKL.AX","TCO.AX","TA1.AX","TCL.AX","XVG.AX","TWE.AX","TKM.AX","TEG.AX","TGF.AX","TBR.AX","TMG.AX","TX3.AX","TT4.AX","TT6.AX","TON.AX","TT3.AX","TRI.AX","TNC.AX","TRM.AX","TRU.AX","TTA.AX","TUA.AX","TGN.AX","TCG.AX","TRA.AX","TYX.AX","TYR.AX","TZL.AX","URW.AX","USL.AX","UOS.AX","UNT.AX","UBI.AX","UNI.AX","UBN.AX","URF.AX","USQ.AX","UCM.AX","UVA.AX","VAL.AX","VR8.AX","VAR.AX","VMG.AX","VR1.AX","VBS.AX","VEE.AX","VNT.AX","VMS.AX","VMC.AX","VBC.AX","VRS.AX","VT2.AX","VTX.AX","VG1.AX","VHM.AX","VCX.AX","VCD.AX","VIG.AX","VTM.AX","VKA.AX","VEN.AX","VNL.AX","VIP.AX","VUK.AX","VMM.AX","VTI.AX","VFX.AX","VGL.AX","VLS.AX","VML.AX","VIT.AX","VEA.AX","VVA.AX","VMT.AX","VPG.AX","VHT.AX","VPR.AX","VRC.AX","VSR.AX","VN8.AX","VRX.AX","VUL.AX","VSL.AX","VYS.AX","WAK.AX","WA1.AX","WGN.AX","WKT.AX","WAA.AX","WMA.AX","WAM.AX","WGB.AX","WLE.AX","WMI.AX","WAX.AX","WAR.AX","WA8.AX","SOL.AX","WAT.AX","W2V.AX","WPR.AX","WQG.AX","WEF.AX","WCG.AX","WEB.AX","WBT.AX","WLD.AX","WFL.AX","WNX.AX","WES.AX","WAF.AX","WC1.AX","WWI.AX","WSR.AX","WER.AX","WGR.AX","WMG.AX","WYX.AX","WEN.AX","WGX.AX","WBC.AX","WSI.AX","WSP.AX","WCN.AX","WEC.AX","WRM.AX","WBE.AX","WHF.AX","WHC.AX","WHK.AX","WIA.AX","WOA.AX","WIN.AX","WC8.AX","WMC.AX","WEL.AX","WNR.AX","WR1.AX","WTN.AX","WTC.AX","WWG.AX","WZR.AX","WDS.AX","WOW.AX","WML.AX","WOR.AX","WOT.AX","WRK.AX","WTL.AX","X2M.AX","XGL.AX","XAM.AX","XRO.AX","XL8.AX","XPN.AX","XRG.AX","XF1.AX","XRF.AX","XST.AX","XTC.AX","YAL.AX","YRL.AX","YAR.AX","YOJ.AX","YOW.AX","YPB.AX","ZLD.AX","ZNC.AX","ZEO.AX","ZER.AX","ZEU.AX","ZGL.AX","ZMM.AX","ZIM.AX","ZMI.AX","ZIP.AX","Z2U.AX","ZNO.AX","ZAG.AX"]
stocks = yf.download(ticker, start=sd, end=ed)
filter_ma = int(115)
close = stocks.loc[:, "Close"].copy()
volume = stocks.loc[:, "Volume"].copy()

# Calculate the 5-day average volume for each stock
average_volume = stocks.loc[:, "Volume"].rolling(window=5).mean()
average_dollar_volume = average_volume * close
# Convert the volume threshold to the currency of the stock prices
volume_threshold = 25000

# Create a directory to save the images
if not os.path.exists('images'):
    os.makedirs('images')

# Part 1: Find the trend of all stocks look to filter further using volume analysis - gradual increase?
trends = {}
std_dev = {}
last_30_days_close = {}
ticker = [stock for stock in ticker if stock in close and not np.isnan(close[stock].iloc[-1]) and average_dollar_volume[stock].iloc[-1] > volume_threshold]

for stock in ticker:
    # Check if there are enough data points
    lookback_days = 250
    if len(close[stock]) > lookback_days:
        # Get the closing price 250 days ago

        past_close = close[stock].iloc[-lookback_days]

        # If the past_close is NaN, look further back until we find a valid price
        while np.isnan(past_close) and lookback_days < len(close[stock]):
            lookback_days += 1
            past_close = close[stock].iloc[-lookback_days]
    # Get the most recent closing price
    last_close = close[stock].iloc[-1]
    # Determine the trend
    if last_close > past_close:
        trends[stock] = "uptrend"
    else:
        trends[stock] = "downtrend"

# Part 2: Calculate Fibonacci levels for each stock based on its trend
fibonacci_levels = {}
for stock, trend in trends.items():
    high = stocks['High', stock].rolling(window=filter_ma).max().iloc[-1]
    low = stocks['Low', stock].rolling(window=filter_ma).min().iloc[-1]
    if trend == "uptrend":
        fibonacci_levels[stock] = [high - level * (high - low) for level in [0.50, 0.618]]  # Correct order for uptrend
    elif trend == "downtrend":
        fibonacci_levels[stock] = [low + level * (high - low) for level in [0.618, 0.50]]  # Correct order for downtrend

# Part 3: Calculate On-Balance Volume (OBV)
obv_values = {}
for stock in ticker:
    obv = np.where(close[stock].diff() > 0, volume[stock], np.where(close[stock].diff() < 0, -volume[stock], 0))
    obv_values[stock] = np.cumsum(obv)

# Convert start_date and end_date to Timestamp objects
start_date = pd.Timestamp(sd)
end_date = pd.Timestamp(ed)

# Part 4: Plot the results with OBV as a subplot
for stock, fibonacci_values in fibonacci_levels.items():
    last_close = close[stock].iloc[-1]
    trend = trends[stock]  # Get the updated trend value
    if min(fibonacci_values) <= last_close <= max(fibonacci_values):
        rsi_series = calculate_rsi(close[stock], 15)
        last_rsi = float(rsi_series.iloc[-1])
        last_30_days_close = close[stock].tail(30)
        std_dev = float(last_30_days_close.std())
        # Calculate EMAs
        ema10 = close[stock].rolling(window=10).mean()
        ema50 = close[stock].rolling(window=50).mean()

        # Filter based on trend and RSI
        if trend == "uptrend" and last_rsi <= 40:
            # Filter OBV data for the specified period
            date_mask = (stocks.index >= start_date) & (stocks.index <= end_date)
            obv_data_filtered = obv_values[stock][date_mask]

            # Create a subplot
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

            # Plot closing prices with Fibonacci lines
            ax1.plot(close[stock])
            ax1.axhline(y=fibonacci_values[0], color='red', linewidth=2, label='Fibonacci 0.50')
            ax1.axhline(y=fibonacci_values[1], color='gold', linewidth=2, label='Fibonacci 0.618')
            ax1.plot(ema10, label='EMA10', color='green', linestyle='--')
            ax1.plot(ema50, label='EMA50', color='purple', linestyle='--')
            ax1.set_title(f'{stock} - Uptrend - RSI: {last_rsi:.2f} - Standard Deviation: {std_dev:.4f}')
            ax1.legend(loc='upper left')

            # Plot OBV with filtered data
            ax2.plot(stocks.index[date_mask], obv_data_filtered, color='blue', label='OBV')
            ax2.set_title('On-Balance Volume (OBV)')
            ax2.legend(loc='upper left')

            plt.savefig(f'images/{stock} - Uptrend - {formatted_date}.png')
            plt.close()

        elif trend == "downtrend" and last_rsi >= 70:
            # Filter OBV data for the specified period
            date_mask = (stocks.index >= start_date) & (stocks.index <= end_date)
            obv_data_filtered = obv_values[stock][date_mask]

            # Create a subplot
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

            # Plot closing prices with Fibonacci lines
            ax1.plot(close[stock])
            ax1.axhline(y=fibonacci_values[0], color='gold', linewidth=2, label='Fibonacci 0.618')
            ax1.axhline(y=fibonacci_values[1], color='red', linewidth=2, label='Fibonacci 0.50')
            ax1.plot(ema10, label='EMA10', color='green', linestyle='--')
            ax1.plot(ema50, label='EMA50', color='purple', linestyle='--')
            ax1.set_title(f'{stock} - Downtrend - RSI: {last_rsi:.2f} - Standard Deviation: {std_dev:.4f}')
            ax1.legend(loc='upper left')

            # Plot OBV with filtered data
            ax2.plot(stocks.index[date_mask], obv_data_filtered, color='blue', label='OBV')
            ax2.set_title('On-Balance Volume (OBV)')
            ax2.legend(loc='upper left')

            plt.savefig(f'images/{stock} - Downtrend - {formatted_date}.png')
            plt.close()