public class Patient implements Comparable<Patient>{
  private int severityID;
  private String patientName;
  private String conditionName;
  public Patient(int severity, String name, String condition) {
     severityID = severity;
     patientName = name;
     conditionName = condition;
}

public int getSeverityID() { return severityID; }
public String getPatientName() { return patientName; }
public String getConditionName() { return conditionName; }

public boolean equals(Patient theOtherPatient) {
  return this.getSeverityID() == theOtherPatient.getSeverityID();
}

@Override
public int compareTo(Patient theOtherPatient) {
  if (this.equals(theOtherPatient))
    return 0;
  else if (getSeverityID() > theOtherPatient.getSeverityID())
    return 1;
  else
    return -1;
}

public String toString() {
  return "Next Patient (" + getSeverityID() +"): " +
     getPatientName() + "\tCondition: " +
     getConditionName();
}


}