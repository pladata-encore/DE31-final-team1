# Environment Define

variable "AIRFLOW_DATABASE_PASSWORD" {
  type        = string
  description = "AIRFLOW DATABASE PASSWORD"
}

variable "AIRFLOW_EMAIL" {
  type        = string
  description = "AIRFLOW EMAIL"
}

variable "AIRFLOW_FERNET_KEY" {
  type        = string
  description = "AIRFLOW FERNET KEY"
}

variable "AIRFLOW_PASSWORD" {
  type        = string
  description = "AIRFLOW PASSWORD"
}

variable "AIRFLOW_SECRET_KEY" {
  type        = string
  description = "AIRFLOW SECRET KEY"
}

variable "AIRFLOW_USERNAME" {
  type        = string
  description = "AIRFLOW USERNAME"
}

variable "POSTGRESQL_DATABASE" {
  type        = string
  description = "POSTGRESQL DATABASE"
}

variable "POSTGRESQL_PASSWORD" {
  type        = string
  description = "POSTGRESQL PASSWORD"
}

variable "POSTGRESQL_USERNAME" {
  type        = string
  description = "POSTGRESQL USERNAME"
}

variable "KAFKA_BOOTSTRAP_SERVERS" {
  type        = string
  description = "Kafka bootstrap servers"
}

variable "MONGO" {
  type        = string
  description = "MongoDB connection string"
}

variable "MONGO_COLLECTION_NAME" {
  type        = string
  description = "MongoDB collection name"
}

variable "MONGO_DATABASE_NAME" {
  type        = string
  description = "MongoDB database name"
}

variable "MONGO_URI" {
  type        = string
  description = "MongoDB URI"
}

variable "MYSQL_URI" {
  type        = string
  description = "MySQL URI"
}

variable "NIFI_URL" {
  type        = string
  description = "NiFi URL"
}