console.log("App Ready");

d3.select("#doCheckTicket").on("click", (event) => doCheckTicket(event));

d3.select("#alertOutcome").style("display", "none");

function doCheckTicket(event) {
    d3.event.preventDefault();
    d3.select("#alertOutcome").style("display", "none");
    console.log("Checking household risk");
 //======================ROW 1 of INPUT Variables===========================================
    let femaleh = d3.select("#femaleh").node().value;
    let hhsize = d3.select("#inputhhsize").node().value;
    let rural = d3.select("#rural").node().value;

//=====================ROW 2 of INPUT Variables============================================
    let Low_education = d3.select("#low_education").node().value;
    let Low_income = d3.select("#low_income").node().value;
    let region = d3.select("#region").node().value;
    let Childlabour_05 = d3.select("#childlabour_05").node().value;

//=====================ROW 3 of INPUT Variables============================================
    age_0t6 = d3.select("#age_0t6").node().value;
    age_7t12 = d3.select("#age_7t12").node().value;
    age_13t15 = d3.select("#age_13t15").node().value;

//=====================ROW 4 of INPUT Variables============================================
    age_16t18 = d3.select("#age_16t18").node().value;
    age_19t60 = d3.select("#age_19t60").node().value;
    age_61 = d3.select("#age_61").node().value;




    let data = {
        "femaleh": femaleh,
        "hhsize": parseFloat(hhsize),
        "rural": rural,
        "Low_education": Low_education,
        "Low_income": Low_income,
        "region": region,
        "Childlabour_05": Childlabour_05,
        "age_0t6": parseFloat(age_0t6)/parseFloat(hhsize),
        "age_7t12": parseFloat(age_7t12)/parseFloat(hhsize),
        "age_13t15": parseFloat(age_13t15)/parseFloat(hhsize),
        "age_16t18": parseFloat(age_16t18)/parseFloat(hhsize),
        "age_19t60": parseFloat(age_19t60)/parseFloat(hhsize),
        "age_61": parseFloat(age_61)/parseFloat(hhsize),
    }

    console.log(data);

    d3.json(
        "/predict", {
            method: "POST",
            body: JSON.stringify(data),
            headers: {
                "Content-type": "application/json; charset=UTF-8"
            }
        }
    ).then(
        (data) => showResult(data)
    );

}

function showResult(data) {
    console.log("showResult");
    console.log(data);

    var outcome = "Unknown";
    let alertOutcomeDisplay = d3.select("#alertOutcome");

    if (data["result"][0] == 1) {
        outcome = "Household at risk";
        alertOutcomeDisplay.attr("class", "alert alert-danger");
    } else if (data["result"][0] == 0) {
        outcome = "Household not at high risk";
        alertOutcomeDisplay.attr("class", "alert alert-success");
    }

    alertOutcomeDisplay.text(outcome);
    alertOutcomeDisplay.style("display", "block");

}