export type MessagingChannel = 'chat' | 'sms';

export interface Stage {
  id: number;
  name: string;
  description: string;
}

export interface StageStatus {
  [stageId: number]: boolean;
}

export interface Patient {
  id: string;
  name: string;
  contact: string;
  preferredChannel: MessagingChannel;
  stageStatus: StageStatus;
  createdAt?: string;
  updatedAt?: string;
}

export interface PatientMessage {
  id: string;
  subject: string;
  body: string;
  channel: MessagingChannel;
  sentAt: string;
}
