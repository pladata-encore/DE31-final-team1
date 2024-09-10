#!/bin/bash

UUID=$(uuidgen)
AUTHORIZATIONS_FILE="/opt/nifi/nifi-current/conf/authorizations.xml"

policy_exists_for_resource() {
  local resource="$1"
  grep -q "resource=\"$resource\"" "$AUTHORIZATIONS_FILE"
}

if ! policy_exists_for_resource "/resources"; then
  NEW_POLICY="<policy identifier=\"$UUID\" resource=\"/resources\" action=\"R\"><user identifier=\"21232f29-7a57-35a7-8389-4a0e4a801fc3\"/></policy>"

  sed -i "/<policies>/a $NEW_POLICY" "$AUTHORIZATIONS_FILE"
fi

if ! policy_exists_for_resource "/provenance"; then
  {
    echo "<policy identifier=\"policy-id-provenance-read\" resource=\"/provenance\" action=\"R\">"
    echo "    <user identifier=\"21232f29-7a57-35a7-8389-4a0e4a801fc3\"/>"
    echo "</policy>"
  } >> "$AUTHORIZATIONS_FILE"
fi

if ! policy_exists_for_resource "/provenance"; then
  {
    echo "<policy identifier=\"policy-id-provenance-write\" resource=\"/provenance\" action=\"W\">"
    echo "    <user identifier=\"21232f29-7a57-35a7-8389-4a0e4a801fc3\"/>"
    echo "</policy>"
  } >> "$AUTHORIZATIONS_FILE"
fi

exec /opt/nifi/nifi-current/bin/nifi.sh start
