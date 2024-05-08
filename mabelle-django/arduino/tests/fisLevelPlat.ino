//***********************************************************************
// Matlab .fis to arduino C converter v2.0.1.25122016                   
// - Karthik Nadig, USA                                                  
// Please report bugs to:                                                
// https://github.com/karthiknadig/ArduinoFIS/issues                     
// If you don't have a GitHub account mail to karthiknadig@gmail.com     
//***********************************************************************

#include "fis_header.h"

// Number of inputs to the fuzzy inference system
const int fis_gcI = 2;
// Number of outputs to the fuzzy inference system
const int fis_gcO = 3;
// Number of rules to the fuzzy inference system
const int fis_gcR = 25;

FIS_TYPE g_fisInput[fis_gcI];
FIS_TYPE g_fisOutput[fis_gcO];

// Setup routine runs once when you press reset:
void setup()
{
    // initialize the Analog pins for input.
    // Pin mode for Input: PitchAngle
    pinMode(0 , INPUT);
    // Pin mode for Input: RollAngle
    pinMode(1 , INPUT);


    // initialize the Analog pins for output.
    // Pin mode for Output: Servo1
    pinMode(2 , OUTPUT);
    // Pin mode for Output: Servo2
    pinMode(3 , OUTPUT);
    // Pin mode for Output: Servo3
    pinMode(4 , OUTPUT);

}

// Loop routine runs over and over again forever:
void loop()
{
    // Read Input: PitchAngle
    g_fisInput[0] = analogRead(0);
    // Read Input: RollAngle
    g_fisInput[1] = analogRead(1);

    g_fisOutput[0] = 0;
    g_fisOutput[1] = 0;
    g_fisOutput[2] = 0;

    fis_evaluate();

    // Set output vlaue: Servo1
    analogWrite(2 , g_fisOutput[0]);
    // Set output vlaue: Servo2
    analogWrite(3 , g_fisOutput[1]);
    // Set output vlaue: Servo3
    analogWrite(4 , g_fisOutput[2]);

}

//***********************************************************************
// Support functions for Fuzzy Inference System                          
//***********************************************************************
// Trapezoidal Member Function
FIS_TYPE fis_trapmf(FIS_TYPE x, FIS_TYPE* p)
{
    FIS_TYPE a = p[0], b = p[1], c = p[2], d = p[3];
    FIS_TYPE t1 = ((x <= c) ? 1 : ((d < x) ? 0 : ((c != d) ? ((d - x) / (d - c)) : 0)));
    FIS_TYPE t2 = ((b <= x) ? 1 : ((x < a) ? 0 : ((a != b) ? ((x - a) / (b - a)) : 0)));
    return (FIS_TYPE) min(t1, t2);
}

// Triangular Member Function
FIS_TYPE fis_trimf(FIS_TYPE x, FIS_TYPE* p)
{
    FIS_TYPE a = p[0], b = p[1], c = p[2];
    FIS_TYPE t1 = (x - a) / (b - a);
    FIS_TYPE t2 = (c - x) / (c - b);
    if ((a == b) && (b == c)) return (FIS_TYPE) (x == a);
    if (a == b) return (FIS_TYPE) (t2*(b <= x)*(x <= c));
    if (b == c) return (FIS_TYPE) (t1*(a <= x)*(x <= b));
    t1 = min(t1, t2);
    return (FIS_TYPE) max(t1, 0);
}

FIS_TYPE fis_min(FIS_TYPE a, FIS_TYPE b)
{
    return min(a, b);
}

FIS_TYPE fis_max(FIS_TYPE a, FIS_TYPE b)
{
    return max(a, b);
}

FIS_TYPE fis_array_operation(FIS_TYPE *array, int size, _FIS_ARR_OP pfnOp)
{
    int i;
    FIS_TYPE ret = 0;

    if (size == 0) return ret;
    if (size == 1) return array[0];

    ret = array[0];
    for (i = 1; i < size; i++)
    {
        ret = (*pfnOp)(ret, array[i]);
    }

    return ret;
}


//***********************************************************************
// Data for Fuzzy Inference System                                       
//***********************************************************************
// Pointers to the implementations of member functions
_FIS_MF fis_gMF[] =
{
    fis_trapmf, fis_trimf
};

// Count of member function for each Input
int fis_gIMFCount[] = { 5, 5 };

// Count of member function for each Output 
int fis_gOMFCount[] = { 5, 5, 5 };

// Coefficients for the Input Member Functions
FIS_TYPE fis_gMFI0Coeff1[] = { -90, -45, -25, -15 };
FIS_TYPE fis_gMFI0Coeff2[] = { -5, 0, 5 };
FIS_TYPE fis_gMFI0Coeff3[] = { -25, -10, 0 };
FIS_TYPE fis_gMFI0Coeff4[] = { 15, 25, 45, 90 };
FIS_TYPE fis_gMFI0Coeff5[] = { 0, 10, 25 };
FIS_TYPE* fis_gMFI0Coeff[] = { fis_gMFI0Coeff1, fis_gMFI0Coeff2, fis_gMFI0Coeff3, fis_gMFI0Coeff4, fis_gMFI0Coeff5 };
FIS_TYPE fis_gMFI1Coeff1[] = { -90, -45, -25, -15 };
FIS_TYPE fis_gMFI1Coeff2[] = { -25, -10, 0 };
FIS_TYPE fis_gMFI1Coeff3[] = { -5, 0, 5 };
FIS_TYPE fis_gMFI1Coeff4[] = { 0, 15, 25 };
FIS_TYPE fis_gMFI1Coeff5[] = { 15, 25, 45, 90 };
FIS_TYPE* fis_gMFI1Coeff[] = { fis_gMFI1Coeff1, fis_gMFI1Coeff2, fis_gMFI1Coeff3, fis_gMFI1Coeff4, fis_gMFI1Coeff5 };
FIS_TYPE** fis_gMFICoeff[] = { fis_gMFI0Coeff, fis_gMFI1Coeff };

// Coefficients for the Output Member Functions
FIS_TYPE fis_gMFO0Coeff1[] = { -3.125, 8.542, 11.46, 23.12 };
FIS_TYPE fis_gMFO0Coeff2[] = { 12.9166666666667, 27.5, 42.0833333333333 };
FIS_TYPE fis_gMFO0Coeff3[] = { 30.4166666666667, 45, 59.5833333333333 };
FIS_TYPE fis_gMFO0Coeff4[] = { 47.9166666666667, 62.5, 77.0833333333333 };
FIS_TYPE fis_gMFO0Coeff5[] = { 66.88, 78.54, 81.46, 93.12 };
FIS_TYPE* fis_gMFO0Coeff[] = { fis_gMFO0Coeff1, fis_gMFO0Coeff2, fis_gMFO0Coeff3, fis_gMFO0Coeff4, fis_gMFO0Coeff5 };
FIS_TYPE fis_gMFO1Coeff1[] = { -3.125, 8.542, 11.46, 23.12 };
FIS_TYPE fis_gMFO1Coeff2[] = { 12.9166666666667, 27.5, 42.0833333333333 };
FIS_TYPE fis_gMFO1Coeff3[] = { 30.4166666666667, 45, 59.5833333333333 };
FIS_TYPE fis_gMFO1Coeff4[] = { 47.9166666666667, 62.5, 77.0833333333333 };
FIS_TYPE fis_gMFO1Coeff5[] = { 66.88, 78.54, 81.46, 93.12 };
FIS_TYPE* fis_gMFO1Coeff[] = { fis_gMFO1Coeff1, fis_gMFO1Coeff2, fis_gMFO1Coeff3, fis_gMFO1Coeff4, fis_gMFO1Coeff5 };
FIS_TYPE fis_gMFO2Coeff1[] = { -3.125, 8.542, 11.46, 23.12 };
FIS_TYPE fis_gMFO2Coeff2[] = { 12.9166666666667, 27.5, 42.0833333333333 };
FIS_TYPE fis_gMFO2Coeff3[] = { 30.4166666666667, 45, 59.5833333333333 };
FIS_TYPE fis_gMFO2Coeff4[] = { 47.9166666666667, 62.5, 77.0833333333333 };
FIS_TYPE fis_gMFO2Coeff5[] = { 66.88, 78.54, 81.46, 93.12 };
FIS_TYPE* fis_gMFO2Coeff[] = { fis_gMFO2Coeff1, fis_gMFO2Coeff2, fis_gMFO2Coeff3, fis_gMFO2Coeff4, fis_gMFO2Coeff5 };
FIS_TYPE** fis_gMFOCoeff[] = { fis_gMFO0Coeff, fis_gMFO1Coeff, fis_gMFO2Coeff };

// Input membership function set
int fis_gMFI0[] = { 0, 1, 1, 0, 1 };
int fis_gMFI1[] = { 0, 1, 1, 1, 0 };
int* fis_gMFI[] = { fis_gMFI0, fis_gMFI1};

// Output membership function set
int fis_gMFO0[] = { 0, 1, 1, 1, 0 };
int fis_gMFO1[] = { 0, 1, 1, 1, 0 };
int fis_gMFO2[] = { 0, 1, 1, 1, 0 };
int* fis_gMFO[] = { fis_gMFO0, fis_gMFO1, fis_gMFO2};

// Rule Weights
FIS_TYPE fis_gRWeight[] = { 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 };

// Rule Type
int fis_gRType[] = { 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 };

// Rule Inputs
int fis_gRI0[] = { 2, 3 };
int fis_gRI1[] = { 2, 4 };
int fis_gRI2[] = { 2, 2 };
int fis_gRI3[] = { 3, 3 };
int fis_gRI4[] = { 3, 4 };
int fis_gRI5[] = { 3, 2 };
int fis_gRI6[] = { 5, 3 };
int fis_gRI7[] = { 5, 4 };
int fis_gRI8[] = { 5, 2 };
int fis_gRI9[] = { 4, 3 };
int fis_gRI10[] = { 4, 5 };
int fis_gRI11[] = { 4, 1 };
int fis_gRI12[] = { 1, 3 };
int fis_gRI13[] = { 1, 5 };
int fis_gRI14[] = { 1, 1 };
int fis_gRI15[] = { 2, 5 };
int fis_gRI16[] = { 2, 1 };
int fis_gRI17[] = { 4, 2 };
int fis_gRI18[] = { 4, 4 };
int fis_gRI19[] = { 1, 4 };
int fis_gRI20[] = { 1, 2 };
int fis_gRI21[] = { 5, 1 };
int fis_gRI22[] = { 5, 5 };
int fis_gRI23[] = { 3, 1 };
int fis_gRI24[] = { 3, 5 };
int* fis_gRI[] = { fis_gRI0, fis_gRI1, fis_gRI2, fis_gRI3, fis_gRI4, fis_gRI5, fis_gRI6, fis_gRI7, fis_gRI8, fis_gRI9, fis_gRI10, fis_gRI11, fis_gRI12, fis_gRI13, fis_gRI14, fis_gRI15, fis_gRI16, fis_gRI17, fis_gRI18, fis_gRI19, fis_gRI20, fis_gRI21, fis_gRI22, fis_gRI23, fis_gRI24 };

// Rule Outputs
int fis_gRO0[] = { 3, 3, 3 };
int fis_gRO1[] = { 2, 4, 4 };
int fis_gRO2[] = { 4, 2, 2 };
int fis_gRO3[] = { 3, 4, 2 };
int fis_gRO4[] = { 3, 4, 3 };
int fis_gRO5[] = { 3, 3, 2 };
int fis_gRO6[] = { 3, 2, 4 };
int fis_gRO7[] = { 3, 3, 4 };
int fis_gRO8[] = { 3, 2, 3 };
int fis_gRO9[] = { 3, 1, 5 };
int fis_gRO10[] = { 3, 3, 5 };
int fis_gRO11[] = { 3, 1, 3 };
int fis_gRO12[] = { 3, 5, 1 };
int fis_gRO13[] = { 3, 5, 3 };
int fis_gRO14[] = { 3, 3, 1 };
int fis_gRO15[] = { 1, 5, 5 };
int fis_gRO16[] = { 5, 1, 1 };
int fis_gRO17[] = { 4, 1, 2 };
int fis_gRO18[] = { 2, 4, 5 };
int fis_gRO19[] = { 2, 4, 1 };
int fis_gRO20[] = { 2, 2, 1 };
int fis_gRO21[] = { 5, 2, 2 };
int fis_gRO22[] = { 1, 4, 4 };
int fis_gRO23[] = { 5, 1, 2 };
int fis_gRO24[] = { 1, 5, 2 };
int* fis_gRO[] = { fis_gRO0, fis_gRO1, fis_gRO2, fis_gRO3, fis_gRO4, fis_gRO5, fis_gRO6, fis_gRO7, fis_gRO8, fis_gRO9, fis_gRO10, fis_gRO11, fis_gRO12, fis_gRO13, fis_gRO14, fis_gRO15, fis_gRO16, fis_gRO17, fis_gRO18, fis_gRO19, fis_gRO20, fis_gRO21, fis_gRO22, fis_gRO23, fis_gRO24 };

// Input range Min
FIS_TYPE fis_gIMin[] = { -45, -45 };

// Input range Max
FIS_TYPE fis_gIMax[] = { 45, 45 };

// Output range Min
FIS_TYPE fis_gOMin[] = { 10, 10, 10 };

// Output range Max
FIS_TYPE fis_gOMax[] = { 80, 80, 80 };

//***********************************************************************
// Data dependent support functions for Fuzzy Inference System           
//***********************************************************************
FIS_TYPE fis_MF_out(FIS_TYPE** fuzzyRuleSet, FIS_TYPE x, int o)
{
    FIS_TYPE mfOut;
    int r;

    for (r = 0; r < fis_gcR; ++r)
    {
        int index = fis_gRO[r][o];
        if (index > 0)
        {
            index = index - 1;
            mfOut = (fis_gMF[fis_gMFO[o][index]])(x, fis_gMFOCoeff[o][index]);
        }
        else if (index < 0)
        {
            index = -index - 1;
            mfOut = 1 - (fis_gMF[fis_gMFO[o][index]])(x, fis_gMFOCoeff[o][index]);
        }
        else
        {
            mfOut = 0;
        }

        fuzzyRuleSet[0][r] = fis_min(mfOut, fuzzyRuleSet[1][r]);
    }
    return fis_array_operation(fuzzyRuleSet[0], fis_gcR, fis_max);
}

FIS_TYPE fis_defuzz_centroid(FIS_TYPE** fuzzyRuleSet, int o)
{
    FIS_TYPE step = (fis_gOMax[o] - fis_gOMin[o]) / (FIS_RESOLUSION - 1);
    FIS_TYPE area = 0;
    FIS_TYPE momentum = 0;
    FIS_TYPE dist, slice;
    int i;

    // calculate the area under the curve formed by the MF outputs
    for (i = 0; i < FIS_RESOLUSION; ++i){
        dist = fis_gOMin[o] + (step * i);
        slice = step * fis_MF_out(fuzzyRuleSet, dist, o);
        area += slice;
        momentum += slice*dist;
    }

    return ((area == 0) ? ((fis_gOMax[o] + fis_gOMin[o]) / 2) : (momentum / area));
}

//***********************************************************************
// Fuzzy Inference System                                                
//***********************************************************************
void fis_evaluate()
{
    FIS_TYPE fuzzyInput0[] = { 0, 0, 0, 0, 0 };
    FIS_TYPE fuzzyInput1[] = { 0, 0, 0, 0, 0 };
    FIS_TYPE* fuzzyInput[fis_gcI] = { fuzzyInput0, fuzzyInput1, };
    FIS_TYPE fuzzyOutput0[] = { 0, 0, 0, 0, 0 };
    FIS_TYPE fuzzyOutput1[] = { 0, 0, 0, 0, 0 };
    FIS_TYPE fuzzyOutput2[] = { 0, 0, 0, 0, 0 };
    FIS_TYPE* fuzzyOutput[fis_gcO] = { fuzzyOutput0, fuzzyOutput1, fuzzyOutput2, };
    FIS_TYPE fuzzyRules[fis_gcR] = { 0 };
    FIS_TYPE fuzzyFires[fis_gcR] = { 0 };
    FIS_TYPE* fuzzyRuleSet[] = { fuzzyRules, fuzzyFires };
    FIS_TYPE sW = 0;

    // Transforming input to fuzzy Input
    int i, j, r, o;
    for (i = 0; i < fis_gcI; ++i)
    {
        for (j = 0; j < fis_gIMFCount[i]; ++j)
        {
            fuzzyInput[i][j] =
                (fis_gMF[fis_gMFI[i][j]])(g_fisInput[i], fis_gMFICoeff[i][j]);
        }
    }

    int index = 0;
    for (r = 0; r < fis_gcR; ++r)
    {
        if (fis_gRType[r] == 1)
        {
            fuzzyFires[r] = FIS_MAX;
            for (i = 0; i < fis_gcI; ++i)
            {
                index = fis_gRI[r][i];
                if (index > 0)
                    fuzzyFires[r] = fis_min(fuzzyFires[r], fuzzyInput[i][index - 1]);
                else if (index < 0)
                    fuzzyFires[r] = fis_min(fuzzyFires[r], 1 - fuzzyInput[i][-index - 1]);
                else
                    fuzzyFires[r] = fis_min(fuzzyFires[r], 1);
            }
        }
        else
        {
            fuzzyFires[r] = FIS_MIN;
            for (i = 0; i < fis_gcI; ++i)
            {
                index = fis_gRI[r][i];
                if (index > 0)
                    fuzzyFires[r] = fis_max(fuzzyFires[r], fuzzyInput[i][index - 1]);
                else if (index < 0)
                    fuzzyFires[r] = fis_max(fuzzyFires[r], 1 - fuzzyInput[i][-index - 1]);
                else
                    fuzzyFires[r] = fis_max(fuzzyFires[r], 0);
            }
        }

        fuzzyFires[r] = fis_gRWeight[r] * fuzzyFires[r];
        sW += fuzzyFires[r];
    }

    if (sW == 0)
    {
        for (o = 0; o < fis_gcO; ++o)
        {
            g_fisOutput[o] = ((fis_gOMax[o] + fis_gOMin[o]) / 2);
        }
    }
    else
    {
        for (o = 0; o < fis_gcO; ++o)
        {
            g_fisOutput[o] = fis_defuzz_centroid(fuzzyRuleSet, o);
        }
    }
}
