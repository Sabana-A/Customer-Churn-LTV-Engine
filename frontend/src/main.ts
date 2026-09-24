import './style.css'

document.querySelector<HTMLDivElement>('#app')!.innerHTML = `
  <div class="container">
    <h1>Customer Churn & LTV Prediction</h1>
    <p class="subtitle">
      Predict customer churn risk and lifetime value
    </p>

    <div class="form-card">
      <h2>Customer Information</h2>

      <label>Senior Citizen</label>
      <select id="SeniorCitizen">
        <option value="0">No</option>
        <option value="1">Yes</option>
      </select>

      <label>Tenure (Months)</label>
      <input type="number" id="tenure" value="12">

      <label>Monthly Charges</label>
      <input type="number" id="MonthlyCharges" value="70">

      <label>Gender</label>
      <select id="gender_Male">
        <option value="0">Female</option>
        <option value="1">Male</option>
      </select>

      <label>Partner</label>
      <select id="Partner_Yes">
        <option value="0">No</option>
        <option value="1">Yes</option>
      </select>

      <label>Dependents</label>
      <select id="Dependents_Yes">
        <option value="0">No</option>
        <option value="1">Yes</option>
      </select>

      <label>Internet Service</label>
      <select id="InternetService_Fiber_optic">
        <option value="0">DSL</option>
        <option value="1">Fiber Optic</option>
      </select>

      <label>Contract</label>
      <select id="Contract">
        <option value="0">Month-to-month</option>
        <option value="1">One year</option>
        <option value="2">Two year</option>
      </select>

      <button id="predictBtn">Predict Customer</button>

      <div id="result"></div>
    </div>
  </div>
`

const predictBtn =
  document.querySelector<HTMLButtonElement>('#predictBtn')!

const result =
  document.querySelector<HTMLDivElement>('#result')!

predictBtn.addEventListener('click', async () => {

  result.innerHTML = `<p>Predicting...</p>`

  const tenure =
    Number((document.querySelector('#tenure') as HTMLInputElement).value)

  const monthlyCharges =
    Number(
      (document.querySelector('#MonthlyCharges') as HTMLInputElement).value
    )

  const contract =
    Number(
      (document.querySelector('#Contract') as HTMLSelectElement).value
    )

  const data = {
    SeniorCitizen: Number(
      (document.querySelector('#SeniorCitizen') as HTMLSelectElement).value
    ),

    tenure: tenure,

    MonthlyCharges: monthlyCharges,

    gender_Male: Number(
      (document.querySelector('#gender_Male') as HTMLSelectElement).value
    ),

    Partner_Yes: Number(
      (document.querySelector('#Partner_Yes') as HTMLSelectElement).value
    ),

    Dependents_Yes: Number(
      (document.querySelector('#Dependents_Yes') as HTMLSelectElement).value
    ),

    PhoneService_Yes: 1,

    MultipleLines_No_phone_service: 0,

    MultipleLines_Yes: 0,

    InternetService_Fiber_optic: Number(
      (document.querySelector('#InternetService_Fiber_optic') as HTMLSelectElement).value
    ),

    InternetService_No: 0,

    OnlineSecurity_No_internet_service: 0,
    OnlineSecurity_Yes: 0,

    OnlineBackup_No_internet_service: 0,
    OnlineBackup_Yes: 0,

    DeviceProtection_No_internet_service: 0,
    DeviceProtection_Yes: 0,

    TechSupport_No_internet_service: 0,
    TechSupport_Yes: 0,

    StreamingTV_No_internet_service: 0,
    StreamingTV_Yes: 0,

    StreamingMovies_No_internet_service: 0,
    StreamingMovies_Yes: 0,

    Contract_One_year: contract === 1 ? 1 : 0,
    Contract_Two_year: contract === 2 ? 1 : 0,

    PaperlessBilling_Yes: 1,

    PaymentMethod_Credit_card_automatic: 0,
    PaymentMethod_Electronic_check: 1,
    PaymentMethod_Mailed_check: 0,

    TenureGroup_13_24_Months: tenure >= 13 && tenure <= 24 ? 1 : 0,
    TenureGroup_25_48_Months: tenure >= 25 && tenure <= 48 ? 1 : 0,
    TenureGroup_49_72_Months: tenure >= 49 ? 1 : 0
  }

  try {

    const response = await fetch('http://127.0.0.1:8000/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })

    const prediction = await response.json()

    if (!response.ok) {
      throw new Error(JSON.stringify(prediction))
    }

    result.innerHTML = `
      <div class="result-card">
        <h2>Prediction Result</h2>

        <p>
          <strong>Churn Prediction:</strong>
          ${prediction.churn_prediction}
        </p>

        <p>
          <strong>Churn Probability:</strong>
          ${(prediction.churn_probability * 100).toFixed(2)}%
        </p>

        <p>
          <strong>Predicted LTV:</strong>
          ₹${prediction.predicted_ltv.toFixed(2)}
        </p>
      </div>
    `

  } catch (error) {

    console.error(error)

    result.innerHTML = `
      <div class="error">
        <strong>Error:</strong>
        Could not connect to FastAPI.
        <br>
        Make sure your backend is running.
      </div>
    `
  }
})