import { useCallback, useEffect, useMemo, useState } from 'react';
import { addDoc, collection, doc, onSnapshot, orderBy, query, serverTimestamp, updateDoc } from 'firebase/firestore';
import { db } from '../firebase';
import type { MessagingChannel, Patient, PatientMessage } from '../types';
import { STAGES } from '../data/stages';

interface UsePatientsResult {
  patients: Patient[];
  loading: boolean;
  selectPatient: (patientId: string | null) => void;
  selectedPatient: Patient | null;
  messages: PatientMessage[];
  addPatient: () => Promise<void>;
  toggleStage: (stageId: number, value: boolean) => Promise<void>;
  sendMessage: (subject: string, body: string, channel: MessagingChannel) => Promise<void>;
}

const PATIENTS_COLLECTION = 'patients';

export function usePatients(): UsePatientsResult {
  const [patients, setPatients] = useState<Patient[]>([]);
  const [messages, setMessages] = useState<PatientMessage[]>([]);
  const [selectedPatientId, setSelectedPatientId] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const q = query(collection(db, PATIENTS_COLLECTION), orderBy('createdAt', 'desc'));
    const unsubscribe = onSnapshot(q, (snapshot) => {
      const docs = snapshot.docs.map((docSnapshot) => {
        const data = docSnapshot.data();
        const stageStatus = data.stageStatus ?? {};
        STAGES.forEach((stage) => {
          if (!(stage.id in stageStatus)) {
            stageStatus[stage.id] = false;
          }
        });
        return {
          id: docSnapshot.id,
          name: data.name ?? 'Sin nombre',
          contact: data.contact ?? 'Sin contacto',
          preferredChannel: (data.preferredChannel ?? 'chat') as MessagingChannel,
          stageStatus,
          createdAt: data.createdAt?.toDate?.().toISOString?.() ?? null,
          updatedAt: data.updatedAt?.toDate?.().toISOString?.() ?? null
        } satisfies Patient;
      });
      setPatients(docs);
      setLoading(false);
    });
    return () => unsubscribe();
  }, []);

  useEffect(() => {
    if (!selectedPatientId) {
      setMessages([]);
      return;
    }
    const messagesQuery = query(
      collection(db, `${PATIENTS_COLLECTION}/${selectedPatientId}/messages`),
      orderBy('sentAt', 'desc')
    );
    const unsubscribe = onSnapshot(messagesQuery, (snapshot) => {
      const docs = snapshot.docs.map((docSnapshot) => {
        const data = docSnapshot.data();
        return {
          id: docSnapshot.id,
          subject: data.subject ?? '',
          body: data.body ?? '',
          channel: (data.channel ?? 'chat') as MessagingChannel,
          sentAt: data.sentAt?.toDate?.().toISOString?.() ?? new Date().toISOString()
        } satisfies PatientMessage;
      });
      setMessages(docs);
    });
    return () => unsubscribe();
  }, [selectedPatientId]);

  const selectedPatient = useMemo(() => patients.find((patient) => patient.id === selectedPatientId) ?? null, [
    patients,
    selectedPatientId
  ]);

  const selectPatient = useCallback((patientId: string | null) => {
    setSelectedPatientId(patientId);
  }, []);

  const addPatient = useCallback(async () => {
    const name = prompt('Nombre del paciente:');
    if (!name) return;
    const contact = prompt('Contacto (teléfono, email):') ?? '';
    const preferredChannel = (prompt('Canal preferido (chat/sms):', 'chat') ?? 'chat') as MessagingChannel;
    const stageStatus = STAGES.reduce<Record<number, boolean>>((acc, stage) => {
      acc[stage.id] = false;
      return acc;
    }, {});
    await addDoc(collection(db, PATIENTS_COLLECTION), {
      name,
      contact,
      preferredChannel,
      stageStatus,
      createdAt: serverTimestamp(),
      updatedAt: serverTimestamp()
    });
  }, []);

  const toggleStage = useCallback(
    async (stageId: number, value: boolean) => {
      if (!selectedPatientId) return;
      const patientRef = doc(db, PATIENTS_COLLECTION, selectedPatientId);
      await updateDoc(patientRef, {
        [`stageStatus.${stageId}`]: value,
        updatedAt: serverTimestamp()
      });
    },
    [selectedPatientId]
  );

  const sendMessage = useCallback(
    async (subject: string, body: string, channel: MessagingChannel) => {
      if (!selectedPatientId) throw new Error('Selecciona un paciente');
      const messagesRef = collection(db, `${PATIENTS_COLLECTION}/${selectedPatientId}/messages`);
      await addDoc(messagesRef, {
        subject,
        body,
        channel,
        sentAt: serverTimestamp(),
        createdAt: serverTimestamp()
      });
      const patientRef = doc(db, PATIENTS_COLLECTION, selectedPatientId);
      await updateDoc(patientRef, {
        lastMessageAt: serverTimestamp(),
        preferredChannel: channel,
        updatedAt: serverTimestamp()
      });
    },
    [selectedPatientId]
  );

  return {
    patients,
    loading,
    selectPatient,
    selectedPatient,
    messages,
    addPatient,
    toggleStage,
    sendMessage
  };
}
