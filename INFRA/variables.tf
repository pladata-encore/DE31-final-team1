# Environment Define

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