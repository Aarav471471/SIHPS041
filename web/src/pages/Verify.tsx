import React, { useEffect, useState } from "react";
import { useParams, useSearchParams } from "react-router-dom";
import { apiClient } from "@/api/client";
import { ShieldCheck, ShieldAlert, XCircle, Loader2 } from "lucide-react";

export default function Verify() {
  const { cid } = useParams();
  const [searchParams] = useSearchParams();
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const d = searchParams.get("d");
    const s = searchParams.get("s");
    
    let url = `/verify/${cid}`;
    if (d && s) {
      url += `?d=${encodeURIComponent(d)}&s=${encodeURIComponent(s)}`;
    }

    apiClient.get(url)
      .then(res => setData(res.data))
      .catch(err => setData({ status: "ERROR", message: "Network error" }))
      .finally(() => setLoading(false));
  }, [cid, searchParams]);

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center flex-col">
        <Loader2 className="h-10 w-10 text-orange-600 animate-spin mb-4" />
        <p className="text-slate-600">Verifying certificate...</p>
      </div>
    );
  }

  const renderStatus = () => {
    const status = data?.status || "NOT_FOUND";
    
    if (status === "VALID") {
      return (
        <div className="bg-green-50 border-t-4 border-green-500 rounded-b-lg shadow-sm p-6 text-center">
          <ShieldCheck className="h-20 w-20 text-green-500 mx-auto mb-4" />
          <h1 className="text-3xl font-extrabold text-green-700 uppercase tracking-wider">Valid</h1>
          <p className="text-green-800 font-medium mt-2">This safety certificate is verified and active.</p>
        </div>
      );
    }
    if (status === "REVOKED") {
      return (
        <div className="bg-red-50 border-t-4 border-red-600 rounded-b-lg shadow-sm p-6 text-center">
          <XCircle className="h-20 w-20 text-red-600 mx-auto mb-4" />
          <h1 className="text-3xl font-extrabold text-red-700 uppercase tracking-wider">Revoked</h1>
          <p className="text-red-800 font-medium mt-2">This certificate was revoked.</p>
          {data?.revoked_reason && <p className="text-sm text-red-700 mt-1">Reason: {data.revoked_reason}</p>}
        </div>
      );
    }
    if (status === "TAMPERED") {
      return (
        <div className="bg-red-50 border-t-4 border-red-600 rounded-b-lg shadow-sm p-6 text-center">
          <ShieldAlert className="h-20 w-20 text-red-600 mx-auto mb-4" />
          <h1 className="text-3xl font-extrabold text-red-700 uppercase tracking-wider">Tampered</h1>
          <p className="text-red-800 font-medium mt-2">The cryptographic signature is invalid. The QR code was altered.</p>
        </div>
      );
    }
    
    return (
      <div className="bg-slate-100 border-t-4 border-slate-500 rounded-b-lg shadow-sm p-6 text-center">
        <XCircle className="h-20 w-20 text-slate-500 mx-auto mb-4" />
        <h1 className="text-3xl font-extrabold text-slate-700 uppercase tracking-wider">Invalid / Not Found</h1>
        <p className="text-slate-600 font-medium mt-2">This certificate record does not exist.</p>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-slate-100 py-12 px-4 sm:px-6">
      <div className="max-w-md mx-auto">
        {renderStatus()}
        
        {data && data.status === "VALID" && (
          <div className="mt-8 bg-white shadow rounded-lg overflow-hidden">
            <div className="px-4 py-5 sm:px-6 border-b border-slate-200">
              <h3 className="text-lg leading-6 font-medium text-slate-900">Certificate Details</h3>
            </div>
            <div className="px-4 py-5 sm:p-0">
              <dl className="sm:divide-y sm:divide-slate-200">
                <div className="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                  <dt className="text-sm font-medium text-slate-500">Worker Name</dt>
                  <dd className="mt-1 text-sm text-slate-900 sm:mt-0 sm:col-span-2 font-semibold">{data.name}</dd>
                </div>
                <div className="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                  <dt className="text-sm font-medium text-slate-500">Site</dt>
                  <dd className="mt-1 text-sm text-slate-900 sm:mt-0 sm:col-span-2">{data.site}</dd>
                </div>
                <div className="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                  <dt className="text-sm font-medium text-slate-500">Module</dt>
                  <dd className="mt-1 text-sm text-slate-900 sm:mt-0 sm:col-span-2 uppercase">{data.modules?.join(", ")}</dd>
                </div>
                <div className="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                  <dt className="text-sm font-medium text-slate-500">Issued</dt>
                  <dd className="mt-1 text-sm text-slate-900 sm:mt-0 sm:col-span-2">{new Date(data.issued).toLocaleDateString()}</dd>
                </div>
                <div className="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                  <dt className="text-sm font-medium text-slate-500">Expires</dt>
                  <dd className="mt-1 text-sm text-slate-900 sm:mt-0 sm:col-span-2">{new Date(data.expires).toLocaleDateString()}</dd>
                </div>
              </dl>
            </div>
          </div>
        )}
        
        <div className="mt-8 text-center text-sm text-slate-500">
          Powered by Suraksha-AR (Govt of Jharkhand)
        </div>
      </div>
    </div>
  );
}
