const API_URL =
  import.meta.env.VITE_API_URL || "http://127.0.0.1:8000/api";

export async function apiRequest(
  endpoint: string,
  options: RequestInit = {}
) {
  const token = localStorage.getItem("access_token");

  const headers = new Headers(options.headers);

  if (options.body && !headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json");
  }

  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }

  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers,
  });

  const data = await response.json().catch(() => null);

  if (!response.ok) {
    const detail = data?.detail;

    let message = "Something went wrong. Please try again.";

    if (typeof detail === "string") {
      message = detail;
    } else if (Array.isArray(detail)) {
      message = detail
        .map((error) => {
          const field = Array.isArray(error.loc)
            ? error.loc
                .filter((part: unknown) => part !== "body")
                .join(".")
            : "";

          return field
            ? `${field}: ${error.msg || "Invalid value"}`
            : error.msg || "Invalid value";
        })
        .join("; ");
    } else if (detail && typeof detail === "object") {
      message = JSON.stringify(detail);
    }

    throw new Error(message);
  }

  return data;
}

export async function registerUser(
  name: string,
  email: string,
  password: string
) {
  return apiRequest("/auth/register", {
    method: "POST",
    body: JSON.stringify({
      name,
      email,
      password,
    }),
  });
}

export async function loginUser(
  email: string,
  password: string
) {
  return apiRequest("/auth/login", {
    method: "POST",
    body: JSON.stringify({
      email,
      password,
    }),
  });
}

export async function getCurrentUser() {
  return apiRequest("/auth/me");
}

export function logoutUser() {
  localStorage.removeItem("access_token");
  localStorage.removeItem("token_type");
  localStorage.removeItem("user");
}

export async function getHealthProfile() {
  return apiRequest("/health-profile/");
}

export async function updateHealthProfile(profile: {
  date_of_birth?: string | null;
  blood_group?: string | null;
  allergies?: string | null;
  medical_conditions?: string | null;
  current_medications?: string | null;
  emergency_contact_name?: string | null;
  emergency_contact_phone?: string | null;
}) {
  return apiRequest("/health-profile/", {
    method: "PUT",
    body: JSON.stringify(profile),
  });
}

export async function createHealthConcern(
  title: string,
  description: string
) {
  return apiRequest("/health-concerns/", {
    method: "POST",
    body: JSON.stringify({
      title,
      description,
    }),
  });
}

export async function getHealthConcerns() {
  return apiRequest("/health-concerns/");
}

export async function uploadMedicalDocument(file: File) {
  const token = localStorage.getItem("access_token");

  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(
    `${API_URL}/medical-documents/upload`,
    {
      method: "POST",
      headers: token
        ? {
            Authorization: `Bearer ${token}`,
          }
        : {},
      body: formData,
    }
  );

  const data = await response.json().catch(() => null);

  if (!response.ok) {
    const detail = data?.detail;
    throw new Error(
      typeof detail === "string"
        ? detail
        : "Failed to upload medical document."
    );
  }

  return data;
}

export async function getMedicalDocuments() {
  return apiRequest("/medical-documents/");
}

export async function analyzeMedicalDocument(documentId: number) {
  return apiRequest(`/medical-analysis/${documentId}`, {
    method: "POST",
  });
}

export async function getHealthTimeline() {
  return apiRequest("/health-timeline/");
}

export async function createDoctorVisit(visit: {
  concern: string;
  duration: string;
  severity: number;
  changes: string;
  medications?: string;
  documents?: string;
  questions?: string[];
}) {
  return apiRequest("/doctor-visits/", {
    method: "POST",
    body: JSON.stringify(visit),
  });
}

export async function getDoctorVisits() {
  return apiRequest("/doctor-visits/");
}